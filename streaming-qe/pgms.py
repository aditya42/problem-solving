import heapq
from collections import defaultdict, Counter


def merge_events(player_events, network_events):
    i = 0
    j = 0

    result = []

    while i < len(player_events) and j < len(network_events):
        if player_events[i][0] <= network_events[j][0]:
            result.append(player_events[i])
            i += 1
        else:
            result.append(network_events[j])
            j += 1
    result.extend(player_events[i:])
    result.extend(network_events[:j])

    return result


def group_failures(failures):
    result = defaultdict(list)
    for failure in failures:
        key = (failure["browser"], failure["error"])
        result[key].append(failure)
    return dict(result)


def top_k_frequent(errors, k):
    freq = Counter(errors)
    return heapq.nlargest(k, freq.keys(), key=freq.get)


def analyze_streaming_logs(events):
    play_request_time = None
    first_frame_time = None
    buffer_start_time = None

    rebuffer_count = 0
    total_rebuffer_time = 0

    for timestamp, event in events:
        if event == "PLAY_REQUEST":
            play_request_time = timestamp

        elif event == "FIRST_FRAME":
            first_frame_time = timestamp

        elif event == "BUFFER_START":
            buffer_start_time = timestamp
            rebuffer_count += 1

        elif event == "BUFFER_END" and buffer_start_time is not None:
            total_rebuffer_time += timestamp - buffer_start_time
            buffer_start_time = None

    ttff = None

    if play_request_time is not None and first_frame_time is not None:
        ttff = first_frame_time - play_request_time

    return {
        "ttff": ttff,
        "rebuffer_count": rebuffer_count,
        "rebuffer_duration": total_rebuffer_time,
    }


VALID_TRANSITIONS = {
    "IDLE": {"LOADING"},
    "LOADING": {"PLAYING", "ERROR"},
    "PLAYING": {"PAUSED", "BUFFERING", "ENDED", "ERROR"},
    "PAUSED": {"PLAYING", "ENDED"},
    "BUFFERING": {"PLAYING", "ERROR"},
    "ENDED": set(),
    "ERROR": set(),
}


def validate_playback_states(states):
    for i in range(len(states) - 1):
        current_state = states[i]
        next_state = states[i + 1]

        if next_state not in VALID_TRANSITIONS.get(current_state, set()):
            return False, f"Invalid transition:{current_state} -> {next_state}"
    return True, "Valid playback sequence"


if __name__ == "__main__":
    player_events = [(1.0, "PLAY_REQUEST"), (2.5, "FIRST_FRAME"), (8.0, "BUFFER_START")]

    network_events = [
        (1.5, "MANIFEST_200"),
        (2.0, "SEGMENT_200"),
        (8.2, "SEGMENT_TIMEOUT"),
    ]
    print(merge_events(player_events, network_events))

    failures = [
        {"browser": "Safari", "error": "DRM_ERROR"},
        {"browser": "Chrome", "error": "NETWORK_ERROR"},
        {"browser": "Safari", "error": "DRM_ERROR"},
        {"browser": "Safari", "error": "BUFFERING"},
    ]
    print(group_failures(failures))

    errors = [
        "DRM_ERROR",
        "BUFFERING",
        "DRM_ERROR",
        "NETWORK_ERROR",
        "BUFFERING",
        "DRM_ERROR",
    ]

    print(top_k_frequent(errors, 2))

    events = [
        (0.0, "PLAY_REQUEST"),
        (2.4, "FIRST_FRAME"),
        (15.0, "BUFFER_START"),
        (17.5, "BUFFER_END"),
    ]

    print(analyze_streaming_logs(events))

    states = ["IDLE", "LOADING", "PLAYING", "BUFFERING", "PLAYING", "ENDED"]

    print(validate_playback_states(states))
