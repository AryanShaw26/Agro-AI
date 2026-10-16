# Models Directory

Place your trained PyTorch checkpoints and deployment metadata here:
- **Active Production Checkpoint**: `efficientnetv2_s_38class_gradcam_best.pth`
- **Active Deployment Contract**: `efficientnetv2_s_metadata.json`
- **Archived Rollback Checkpoint**: `efficientnet_b0_best.pth` (retained for backward compatibility and rollback safety)

*Note: Heavy model weights (`*.pth`, `*.pt`, `*.onnx`) are excluded from Git version control via `.gitignore`, while the deployment contract `efficientnetv2_s_metadata.json` is tracked.*
