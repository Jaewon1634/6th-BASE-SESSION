import copy
import torch.nn as nn

from models.layer.residual_connection_layer import ResidualConnectionLayer

## Residual(Self Attention + Cross Attention + FFN) 으로 구성된 디코더 블록
class DecoderBlock(nn.Module):

    def __init__(self, self_attention, cross_attention, position_ff, norm, dr_rate=1, gated=True):
        super(DecoderBlock, self).__init__()
        self.self_attention = self_attention
        self.residual1 = ResidualConnectionLayer(copy.deepcopy(norm), dr_rate, gated=gated)
        self.cross_attention = cross_attention
        self.residual2 = ResidualConnectionLayer(copy.deepcopy(norm), dr_rate, gated=gated)
        self.position_ff = position_ff
        self.residual3 = ResidualConnectionLayer(copy.deepcopy(norm), dr_rate, gated=gated)

    def forward(self, tgt, encoder_out, tgt_mask, src_tgt_mask):
        out = tgt
        out = self.residual1(out, lambda out: self.self_attention(query=out, key=out, value=out, mask=tgt_mask))
        out = self.residual2(out, lambda out: self.cross_attention(query=out, key=encoder_out, value=encoder_out, mask=src_tgt_mask))
        out = self.residual3(out, self.position_ff)
        return out