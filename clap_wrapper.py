import sys

import torch
from transformers import ClapModel, ClapProcessor

models = dict()
MODEL_NAME = "laion/clap-htsat-fused"
processor = ClapProcessor.from_pretrained(MODEL_NAME)


def get_clap_audio_feature(audio_data, device="cuda"):
    if (
        sys.platform == "darwin"
        and torch.backends.mps.is_available()
        and device == "cpu"
    ):
        device = "mps"
    if not device:
        device = "cuda"
    if device not in models.keys():
        # if config.webui_config.fp16_run:
        #     models[device] = ClapModel.from_pretrained(
        #         LOCAL_PATH, torch_dtype=torch.float16
        #     ).to(device)
        # else:
        #     models[device] = ClapModel.from_pretrained(LOCAL_PATH).to(device)
        models[device] = ClapModel.from_pretrained(MODEL_NAME).to(device)
    with torch.no_grad():
        inputs = processor(
            audios=audio_data, return_tensors="pt", sampling_rate=48000
        ).to(device)
        emb = models[device].get_audio_features(**inputs).float()
    return emb.T


def get_clap_text_feature(text, device="cuda"):
    if (
        sys.platform == "darwin"
        and torch.backends.mps.is_available()
        and device == "cpu"
    ):
        device = "mps"
    if not device:
        device = "cuda"
    if device not in models.keys():
        # if config.webui_config.fp16_run:
        #     models[device] = ClapModel.from_pretrained(
        #         LOCAL_PATH, torch_dtype=torch.float16
        #     ).to(device)
        # else:
        #     models[device] = ClapModel.from_pretrained(LOCAL_PATH).to(device)
        models[device] = ClapModel.from_pretrained(MODEL_NAME).to(device)
    with torch.no_grad():
        inputs = processor(text=text, return_tensors="pt").to(device)
        emb = models[device].get_text_features(**inputs).float()
    return emb.T
