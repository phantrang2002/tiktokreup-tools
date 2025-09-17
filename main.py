import os
import random
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, vfx
from moviepy.video.fx.all import resize, fadein, fadeout, mirror_x, speedx

# --- Thư mục input và output ---
INPUT_FOLDER = "videos_reup"
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Các file cố định ---
BG_PATH = "ocean.mp4"
LOGO_PATH = "logo.png"

# --- Xử lý từng video ---
for filename in os.listdir(INPUT_FOLDER):
    if not filename.lower().endswith((".mp4", ".mov", ".avi")):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"final_{filename}")

    # Load background và overlay, mute audio
    bg_clip = VideoFileClip(BG_PATH).without_audio()
    overlay_clip = VideoFileClip(input_path).without_audio()

    # Resize background chẵn số
    bg_w = bg_clip.w if bg_clip.w % 2 == 0 else bg_clip.w + 1
    bg_h = bg_clip.h if bg_clip.h % 2 == 0 else bg_clip.h + 1
    bg_clip = resize(bg_clip, width=bg_w, height=bg_h)

    # Resize overlay: chiếm 75% diện tích bg, giữ tỉ lệ
    overlay_scale = 0.75
    target_h = int(bg_h * overlay_scale)
    target_w = int(target_h * overlay_clip.w / overlay_clip.h)
    if target_w % 2 != 0:
        target_w += 1
    overlay = resize(overlay_clip, width=target_w, height=target_h)

    # Flip ngang 50% ngẫu nhiên
    if random.random() > 0.5:
        overlay = mirror_x(overlay)

    # Speed ±0.02
    speed_factor = round(random.uniform(1.03, 1.07), 3)
    overlay = speedx(overlay, factor=speed_factor)

    # Fade in/out 1s
    overlay = fadein(overlay, 1)
    overlay = fadeout(overlay, 1)

    # Opacity 85%
    overlay = overlay.set_opacity(0.85)

    # Chỉnh brightness overlay (tăng 10%)
    overlay = overlay.fl_image(lambda frame: (frame * 1.1).clip(0,255).astype('uint8'))

    # Overlay đặt giữa background
    overlay_x = (bg_w - overlay.w) // 2
    overlay_y = (bg_h - overlay.h) // 2
    overlay = overlay.set_position((overlay_x, overlay_y))

    # Logo góc trên phải của overlay
    logo = ImageClip(LOGO_PATH, duration=overlay.duration)
    logo = resize(logo, height=int(overlay.h * 0.1))  # ~10% chiều cao overlay
    logo = logo.set_opacity(1.0)  # logo rõ
    logo_x = overlay_x + overlay.w - logo.w - 10  # cách viền phải 10px
    logo_y = overlay_y + 10  # cách viền trên 10px
    logo = logo.set_position((logo_x, logo_y))

    # Loop và crop background đúng duration overlay
    n_loops = int((overlay.duration) // bg_clip.duration) + 1
    bg = CompositeVideoClip([bg_clip.set_start(i*bg_clip.duration) for i in range(n_loops)])
    bg = bg.subclip(0, overlay.duration)

    # Composite video: bg + overlay + logo
    final = CompositeVideoClip([bg, overlay, logo])

    # Xuất video, mute audio, xóa metadata
    final.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio=False,  # mute
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-map_metadata", "-1"]
    )

    print(f"😎 Processed {filename} → {output_path}")

print("✅ Hoàn tất tất cả video!")
