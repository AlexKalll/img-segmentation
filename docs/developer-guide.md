# Developer Guide

## Project Structure

```
img-segmentation/
├── app/
│   ├── main.py
│   └── components/
│       ├── sidebar_controls.py
│       └── display_utils.py
├── src/
│   ├── fh_segmentation.py
│   ├── union_find.py
│   ├── image_utils.py
│   └── visualization.py
├── outputs/
├── .streamlit/
│   └── config.toml
├── requirements.txt
└── README.md
```

## Environment

- Python 3.9+
- Install dependencies: `pip install -r requirements.txt`
- Local run: `streamlit run app/main.py`

## Key Modules

- `app/main.py`: entrypoint; orchestrates layout and flow
- `app/components/sidebar_controls.py`: sidebar UI, image selection, parameters
- `app/components/display_utils.py`: UI rendering helpers, progress, and output display
- `src/fh_segmentation.py`: FH algorithm and segment analysis
- `src/image_utils.py`: I/O, sample loading, preprocessing

## Reactive Image Source Handling

- Sidebar persists control state in `st.session_state.controls_state`
- Emits `image_key` that identifies the currently selected image
- Main page compares `image_key` with cached results to decide whether to show Run button or cached outputs

## Adding New Features

- New sidebar control: add to `sidebar_controls.py` and persist to `st.session_state`
- New visualization: add helper to `display_utils.py` and call from `main.py`
- New algorithm: add to `src/`, expose a function, and integrate in `main.py`

## Testing

- Add tests in `tests/` (e.g., unit tests for `src/` functions)
- Keep UI logic thin; prefer testing pure functions in `src/`

## Code Style

- Favor readable names and early returns
- Avoid deep nesting; only add comments for non-obvious logic
- Keep formatting consistent and avoid unrelated refactors
