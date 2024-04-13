"""Return video tuple, first start video index and second end video index."""
import os


video_debug = (43, 46)
debug = False
debug_env_value = os.environ.get("DEBUG")
if not debug and debug_env_value is not None:
    debug = debug_env_value

if debug:
    print(f"Debug mode is turned on, using videos {video_debug}")
ci_youtube_dl_down = False
flask_log = False

# The length of the power hour videos
# If None dont do anything. If an int make them that long.
# This will be useful to set to 1 or something and then
# the download process will be much quicker
main_video_length = None
