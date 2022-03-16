from transformers import AutoModel, AutoConfig, AutoTokenizer
import torch.nn as nn


class Encoder(nn.Module):
    """
    Encoder model using HuggingFace for NLP

    To load your desired model specify model checkpoint under cfg.model.encoder_checkpoint

    Args:
        cfg: An omegaconf.DictConf instance containing all the configurations.
        vocab_size: Total size of the tokens dictionary
    """

    def __init__(self, cfg, **kwargs):
        super(Encoder, self).__init__()
        self.cfg = cfg
        checkpoint = cfg.model.encoder_checkpoint
        model_config = AutoConfig.from_pretrained(checkpoint)
        self.encoder = AutoModel.from_config(model_config)

    def forward(self, src, **kwargs):
        """
        Forward inputs through the encoder and extract transformer/attention layers outputs

        Args:
            src: masked source tokens

        Returns:
            A dictionary of encoder outputs including encoder outputs and attentions outputs

        """
        outputs = self.encoder(src, output_hidden_states=True, output_attentions=True, **kwargs)
        encoder_states = outputs['hidden_states'][:-1]  # encoder layers outputs separately
        encoder_out = outputs['hidden_states'][-1]      # last encoder output (accumulated)
        attentions = outputs['attentions']
        return {
            'encoder_states': encoder_states,
            'encoder_out': encoder_out,
            'attentions': attentions
        }


if __name__ == '__main__':
    from omegaconf import OmegaConf
    cfg = OmegaConf.load('configs/roberta-pretraining.yaml')
    tokenizer = AutoTokenizer.from_pretrained('roberta-base')
    model = Encoder(cfg)
    inputs = tokenizer("The capital of France is <mask>.", return_tensors="pt")
    outputs = model(inputs['input_ids'])
    print(outputs)