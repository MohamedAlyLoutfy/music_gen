from frechet_audio_distance import FrechetAudioDistance

# Initialize with VGGish model
frechet = FrechetAudioDistance(
    model_name="vggish",
    sample_rate=16000,
    use_pca=False,
    use_activation=False,
    verbose=True
)

# Compute FAD score between two **directories**
score = frechet.score(
    background_dir=r"C:\MS4\test_ldm\test4\target",  # folder containing target1.wav
    eval_dir=r"C:\MS4\test_ldm\test4\pre_trained",  # folder with test1.wav
    dtype="float32"
)

print(f"FAD score: {score:.4f}")
