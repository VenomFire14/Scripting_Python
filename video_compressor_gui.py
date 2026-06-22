import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import ffmpeg
import os

def get_video_bitrate(input_file):
    """
    Get the average bitrate (in kbps) of the input video.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "format=bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    bitrate_bps = int(result.stdout)
    bitrate_kbps = bitrate_bps // 1000
    return bitrate_kbps

def compress_by_percentage(input_file, output_file, percentage):
    """
    Compress video to approximately a percentage of original size.
    """
    original_bitrate = get_video_bitrate(input_file)
    print(f"Original bitrate: {original_bitrate} kbps")

    target_bitrate = int(original_bitrate * (percentage / 100.0))
    print(f"Target bitrate: {target_bitrate} kbps")

    audio_bitrate = 128

    try:
        (
            ffmpeg
            .input(input_file)
            .output(
                output_file,
                vcodec='libx264',
                video_bitrate=f"{target_bitrate}k",
                acodec='aac',
                audio_bitrate=f"{audio_bitrate}k",
                movflags='faststart'
            )
            .overwrite_output()
            .run()
        )
        messagebox.showinfo("Success", f"Compression complete!\nSaved to:\n{output_file}")
    except ffmpeg.Error as e:
        messagebox.showerror("Error", f"FFmpeg Error: {e}")

def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                             filetypes=[("MP4 Video", "*.mp4")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def start_compression():
    input_file = input_entry.get()
    output_file = output_entry.get()
    percentage = percentage_entry.get()

    if not input_file or not os.path.exists(input_file):
        messagebox.showerror("Error", "Please select a valid input file.")
        return
    if not output_file:
        messagebox.showerror("Error", "Please select an output file.")
        return
    try:
        percentage_value = float(percentage)
        if not (0 < percentage_value < 100):
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid percentage (1-99).")
        return

    compress_by_percentage(input_file, output_file, percentage_value)

# --- Tkinter GUI ---

root = tk.Tk()
root.title("Video Compressor")

# Input File
tk.Label(root, text="Input File:").grid(row=0, column=0, sticky="e")
input_entry = tk.Entry(root, width=50)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=5)

# Output File
tk.Label(root, text="Output File:").grid(row=1, column=0, sticky="e")
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=5)

# Percentage
tk.Label(root, text="Target Size (% of original):").grid(row=2, column=0, sticky="e")
percentage_entry = tk.Entry(root, width=10)
percentage_entry.insert(0, "50")
percentage_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

# Compress Button
compress_button = tk.Button(root, text="Compress Video", command=start_compression, bg="#4CAF50", fg="white")
compress_button.grid(row=3, column=1, pady=10)

root.mainloop()
