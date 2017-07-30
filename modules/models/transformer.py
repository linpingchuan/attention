import sonnet as snt
import tensorflow as tf

from ..encoders import Encoder
from ..decoders import Decoder


class TransformerModule(snt.AbstractModule):
    def __init__(self, params):
        super(TransformerModule, self).__init__(name="transformer")
        self.params = params

    def _build(self, features):
        encoder_inputs = features[0][0]
        decoder_inputs = features[1][0]

        encoder = Encoder(
            params=self.params.encoder_params.params,
            block_params=self.params.encoder_params.encoder_block_params,
            embed_params=self.params.encoder_params.embed_params
        )

        encoder_output = encoder(inputs=encoder_inputs)

        decoder = Decoder(
            params=self.params.decoder_params.params,
            block_params=self.params.decoder_params.decoder_block_params,
            embed_params=self.params.decoder_params.embed_params
        )

        # TODO: incorrect
        eos_token = self.params.get("eos_token", 0)
        labels = tf.concat([decoder_inputs[:, 1:], tf.expand_dims(tf.ones_like(decoder_inputs[:, 0]), axis=-1) * eos_token], axis=-1)
        loss, _ = decoder(inputs=decoder_inputs, labels=labels, encoder_output=encoder_output)
        return loss
