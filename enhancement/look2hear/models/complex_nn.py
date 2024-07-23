import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

import abc
import re
import six

def expect_token_number(instr, token):
    first_token = re.match(r'^\s*' + token, instr)
    if first_token is None:
        return None
    instr = instr[first_token.end():]
    lr = re.match(r'^\s*(-?\d+\.?\d*e?-?\d*?)', instr)
    if lr is None:
        return None
    return instr[lr.end():], lr.groups()[0]


def expect_kaldi_matrix(instr):
    pos2 = instr.find('[', 0)
    pos3 = instr.find(']', pos2)
    mat = []
    for stt in instr[pos2 + 1:pos3].split('\n'):
        tmp_mat = np.fromstring(stt, dtype=np.float32, sep=' ')
        if tmp_mat.size > 0:
            mat.append(tmp_mat)
    return instr[pos3 + 1:], np.array(mat)



def to_kaldi_matrix(np_mat):
    """ function that transform as str numpy mat to standard kaldi str matrix

    Args:
        np_mat: numpy mat
    """
    np.set_printoptions(threshold=np.inf, linewidth=np.nan)
    out_str = str(np_mat)
    out_str = out_str.replace('[', '')
    out_str = out_str.replace(']', '')
    return '[ %s ]\n' % out_str


@six.add_metaclass(abc.ABCMeta)
class LayerBase(nn.Module):

    def __init__(self):
        super(LayerBase, self).__init__()

    @abc.abstractmethod
    def to_kaldi_nnet(self):
        pass


class UniDeepFsmn(LayerBase):

    def __init__(self, input_dim, output_dim, lorder=1, hidden_size=None):
        super(UniDeepFsmn, self).__init__()

        self.input_dim = input_dim
        self.output_dim = output_dim
        self.lorder = lorder
        self.hidden_size = hidden_size

        self.linear = nn.Linear(input_dim, hidden_size)
        self.project = nn.Linear(hidden_size, output_dim, bias=False)
        self.conv1 = nn.Conv2d(
            output_dim,
            output_dim, (lorder, 1), (1, 1),
            groups=output_dim,
            bias=False)

    def forward(self, input):
        """

        Args:
            input: torch with shape: batch (b) x sequence(T) x feature (h)

        Returns:
            batch (b) x channel (c) x sequence(T) x feature (h)
        """
        f1 = F.relu(self.linear(input))
        p1 = self.project(f1)
        x = torch.unsqueeze(p1, 1)
        # x: batch (b) x channel (c) x sequence(T) x feature (h)
        x_per = x.permute(0, 3, 2, 1)
        # x_per: batch (b) x feature (h) x sequence(T) x channel (c)
        y = F.pad(x_per, [0, 0, self.lorder - 1, 0])

        out = x_per + self.conv1(y)
        out1 = out.permute(0, 3, 2, 1)
        # out1: batch (b) x channel (c) x sequence(T) x feature (h)
        return input + out1.squeeze()

    def to_kaldi_nnet(self):
        re_str = ''
        re_str += '<UniDeepFsmn> %d %d\n'\
                  % (self.output_dim, self.input_dim)
        re_str += '<LearnRateCoef> %d <HidSize> %d <LOrder> %d <LStride> %d <MaxNorm> 0\n'\
                  % (1, self.hidden_size, self.lorder, 1)

        lfiters = self.state_dict()['conv1.weight']
        x = np.flipud(lfiters.squeeze().numpy().T)
        re_str += to_kaldi_matrix(x)
        proj_weights = self.state_dict()['project.weight']
        x = proj_weights.squeeze().numpy()
        re_str += to_kaldi_matrix(x)
        linear_weights = self.state_dict()['linear.weight']
        x = linear_weights.squeeze().numpy()
        re_str += to_kaldi_matrix(x)
        linear_bias = self.state_dict()['linear.bias']
        x = linear_bias.squeeze().numpy()
        re_str += to_kaldi_matrix(x)
        return re_str

    def load_kaldi_nnet(self, instr):
        output = expect_token_number(
            instr,
            '<LearnRateCoef>',
        )
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, lr = output

        output = expect_token_number(
            instr,
            '<HidSize>',
        )
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, hiddensize = output
        self.hidden_size = int(hiddensize)

        output = expect_token_number(
            instr,
            '<LOrder>',
        )
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, lorder = output
        self.lorder = int(lorder)

        output = expect_token_number(
            instr,
            '<LStride>',
        )
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, lstride = output
        self.lstride = lstride

        output = expect_token_number(
            instr,
            '<MaxNorm>',
        )
        if output is None:
            raise Exception('UniDeepFsmn format error')

        output = expect_kaldi_matrix(instr)
        if output is None:
            raise Exception('Fsmn format error')
        instr, mat = output
        mat1 = np.fliplr(mat.T).copy()
        self.conv1 = nn.Conv2d(
            self.output_dim,
            self.output_dim, (self.lorder, 1), (1, 1),
            groups=self.output_dim,
            bias=False)
        mat_th = torch.from_numpy(mat1).type(torch.FloatTensor)
        mat_th = mat_th.unsqueeze(1)
        mat_th = mat_th.unsqueeze(3)
        self.conv1.weight = torch.nn.Parameter(mat_th)

        output = expect_kaldi_matrix(instr)
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, mat = output

        self.project = nn.Linear(self.hidden_size, self.output_dim, bias=False)
        self.linear = nn.Linear(self.input_dim, self.hidden_size)
        self.project.weight = torch.nn.Parameter(
            torch.from_numpy(mat).type(torch.FloatTensor))

        output = expect_kaldi_matrix(instr)
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, mat = output
        self.linear.weight = torch.nn.Parameter(
            torch.from_numpy(mat).type(torch.FloatTensor))

        output = expect_kaldi_matrix(instr)
        if output is None:
            raise Exception('UniDeepFsmn format error')
        instr, mat = output
        self.linear.bias = torch.nn.Parameter(
            torch.from_numpy(mat).type(torch.FloatTensor))
        return instr


class ComplexUniDeepFsmn(nn.Module):

    def __init__(self, nIn, nHidden=128, nOut=128):
        super(ComplexUniDeepFsmn, self).__init__()

        self.fsmn_re_L1 = UniDeepFsmn(nIn, nHidden, 20, nHidden)
        self.fsmn_im_L1 = UniDeepFsmn(nIn, nHidden, 20, nHidden)
        self.fsmn_re_L2 = UniDeepFsmn(nHidden, nOut, 20, nHidden)
        self.fsmn_im_L2 = UniDeepFsmn(nHidden, nOut, 20, nHidden)

    def forward(self, x):
        r"""

        Args:
            x: torch with shape [batch, channel, feature, sequence, 2], eg: [6, 256, 1, 106, 2]

        Returns:
            [batch, feature, sequence, 2], eg: [6, 99, 1024, 2]
        """
        #
        b, c, h, T, d = x.size()
        x = torch.reshape(x, (b, c * h, T, d))
        # x: [b,h,T,2], [6, 256, 106, 2]
        x = torch.transpose(x, 1, 2)
        # x: [b,T,h,2], [6, 106, 256, 2]

        real_L1 = self.fsmn_re_L1(x[..., 0]) - self.fsmn_im_L1(x[..., 1])
        imaginary_L1 = self.fsmn_re_L1(x[..., 1]) + self.fsmn_im_L1(x[..., 0])
        # GRU output: [99, 6, 128]
        real = self.fsmn_re_L2(real_L1) - self.fsmn_im_L2(imaginary_L1)
        imaginary = self.fsmn_re_L2(imaginary_L1) + self.fsmn_im_L2(real_L1)
        # output: [b,T,h,2], [99, 6, 1024, 2]
        output = torch.stack((real, imaginary), dim=-1)

        # output: [b,h,T,2], [6, 99, 1024, 2]
        output = torch.transpose(output, 1, 2)
        output = torch.reshape(output, (b, c, h, T, d))

        return output


class ComplexUniDeepFsmn_L1(nn.Module):

    def __init__(self, nIn, nHidden=128, nOut=128):
        super(ComplexUniDeepFsmn_L1, self).__init__()
        self.fsmn_re_L1 = UniDeepFsmn(nIn, nHidden, 20, nHidden)
        self.fsmn_im_L1 = UniDeepFsmn(nIn, nHidden, 20, nHidden)

    def forward(self, x):
        r"""

        Args:
            x: torch with shape [batch, channel, feature, sequence, 2], eg: [6, 256, 1, 106, 2]
        """
        b, c, h, T, d = x.size()
        # x : [b,T,h,c,2]
        x = torch.transpose(x, 1, 3)
        x = torch.reshape(x, (b * T, h, c, d))

        real = self.fsmn_re_L1(x[..., 0]) - self.fsmn_im_L1(x[..., 1])
        imaginary = self.fsmn_re_L1(x[..., 1]) + self.fsmn_im_L1(x[..., 0])
        # output: [b*T,h,c,2], [6*106, h, 256, 2]
        output = torch.stack((real, imaginary), dim=-1)

        output = torch.reshape(output, (b, T, h, c, d))
        output = torch.transpose(output, 1, 3)
        return output

class ComplexConv2d(nn.Module):
    # https://github.com/litcoderr/ComplexCNN/blob/master/complexcnn/modules.py
    def __init__(self,
                 in_channel,
                 out_channel,
                 kernel_size,
                 stride=1,
                 padding=0,
                 dilation=1,
                 groups=1,
                 bias=True,
                 **kwargs):
        super().__init__()

        # Model components
        self.conv_re = nn.Conv2d(
            in_channel,
            out_channel,
            kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
            **kwargs)
        self.conv_im = nn.Conv2d(
            in_channel,
            out_channel,
            kernel_size,
            stride=stride,
            padding=padding,
            dilation=dilation,
            groups=groups,
            bias=bias,
            **kwargs)

    def forward(self, x):
        r"""

        Args:
            x: torch with shape: [batch,channel,axis1,axis2,2]
        """
        real = self.conv_re(x[..., 0]) - self.conv_im(x[..., 1])
        imaginary = self.conv_re(x[..., 1]) + self.conv_im(x[..., 0])
        output = torch.stack((real, imaginary), dim=-1)
        return output


class ComplexConvTranspose2d(nn.Module):

    def __init__(self,
                 in_channel,
                 out_channel,
                 kernel_size,
                 stride=1,
                 padding=0,
                 output_padding=0,
                 dilation=1,
                 groups=1,
                 bias=True,
                 **kwargs):
        super().__init__()

        # Model components
        self.tconv_re = nn.ConvTranspose2d(
            in_channel,
            out_channel,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            output_padding=output_padding,
            groups=groups,
            bias=bias,
            dilation=dilation,
            **kwargs)
        self.tconv_im = nn.ConvTranspose2d(
            in_channel,
            out_channel,
            kernel_size=kernel_size,
            stride=stride,
            padding=padding,
            output_padding=output_padding,
            groups=groups,
            bias=bias,
            dilation=dilation,
            **kwargs)

    def forward(self, x):  # shpae of x : [batch,channel,axis1,axis2,2]
        real = self.tconv_re(x[..., 0]) - self.tconv_im(x[..., 1])
        imaginary = self.tconv_re(x[..., 1]) + self.tconv_im(x[..., 0])
        output = torch.stack((real, imaginary), dim=-1)
        return output


        
class ComplexBatchNorm2d(nn.Module):

    def __init__(self,
                 num_features,
                 eps=1e-5,
                 momentum=0.1,
                 affine=True,
                 track_running_stats=True,
                 **kwargs):
        super().__init__()
        self.bn_re = nn.BatchNorm2d(
            num_features=num_features,
            momentum=momentum,
            affine=affine,
            eps=eps,
            track_running_stats=track_running_stats,
            **kwargs)
        self.bn_im = nn.BatchNorm2d(
            num_features=num_features,
            momentum=momentum,
            affine=affine,
            eps=eps,
            track_running_stats=track_running_stats,
            **kwargs)

    def forward(self, x):
        real = self.bn_re(x[..., 0])
        imag = self.bn_im(x[..., 1])
        output = torch.stack((real, imag), dim=-1)
        return output
