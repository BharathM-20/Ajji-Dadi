"""Normalize only the explicitly added incoming-demo dispatch for historical app guards."""

import ast
import copy


def without_incoming_dispatch(function):
    function = copy.deepcopy(function)
    expected = ast.parse(
        'if os.environ.get("DADI_INCOMING") == "1":\n    return build_incoming_ui()'
    ).body[0]
    assert ast.dump(function.body[0]) == ast.dump(expected)
    function.body.pop(0)
    return function


def without_prerecorded_samples(function):
    """Ignore only the shared prerecorded-samples presentation call in old UI snapshots."""
    function = copy.deepcopy(function)
    if function.name not in {"build_ui", "build_local_ui", "build_speech_ui"}:
        return function
    expected = ast.parse("add_prerecorded_samples()").body[0]
    removed = []

    def visit(node):
        for _, value in ast.iter_fields(node):
            if not isinstance(value, list):
                continue
            for index in range(len(value) - 1, -1, -1):
                if ast.dump(value[index]) == ast.dump(expected):
                    assert index > 0 and "showcase.INTRO" in ast.unparse(value[index - 1])
                    value.pop(index)
                    removed.append(True)
                elif isinstance(value[index], ast.AST):
                    visit(value[index])

    visit(function)
    assert len(removed) == 1
    return function


def without_summary_dispatch(function):
    function = copy.deepcopy(function)
    expected = ast.parse(
        'if adapters.sarvam_enabled() or state.get("sarvam_source"):\n'
        '    report = call_summary.finish(state)\n'
        '    return (*speech_view(state), report, call_summary.write_txt_report(state))'
    ).body[0]
    assert ast.dump(function.body[0]) == ast.dump(expected)
    function.body.pop(0)
    return function


def without_stt_ui_additions(function):
    """Remove only the explicit recovery UI additions; freeze the old handler body."""
    if function.name == "speech_view":
        function = copy.deepcopy(function)
        expected = ast.parse('result[3] += "\\n\\n" + speech_brain_route()').body[0]
        assert ast.dump(function.body[1]) == ast.dump(expected)
        function.body.pop(1)
    function = without_brief_ui_additions(function)
    if function.name == "build_speech_ui":
        status = next(
            node for node in ast.walk(function)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "status"
                for target in node.targets
            )
        )
        expected = ast.parse(
            'gr.Markdown("Mode: SCREEN\\n\\n" + speech_brain_route(), elem_id="call-status")'
        ).body[0].value
        assert ast.dump(status.value) == ast.dump(expected)
        status.value.args[0] = ast.Constant(value="Mode: SCREEN")
    if function.name == "speech_end":
        expected = ast.parse('state.pop("stt_retry", None)').body[0]
        assert ast.dump(function.body[0]) == ast.dump(expected)
        function.body.pop(0)
    elif function.name == "speech_reset":
        expected = ast.parse(
            'return (*speech_view(local_brain.new_state()), "", None)'
        ).body[0]
        assert ast.dump(function.body[0]) == ast.dump(expected)
        function.body[0].value.elts.pop()
    elif function.name == "speech_turn":
        assert function.args.args[-1].arg == "inspect_only"
        assert ast.literal_eval(function.args.defaults[-1]) is False
        function.args.args.pop()
        function.args.defaults.pop()
        expected_branch = ast.parse('''
if inspect_only:
    state, audio = speech_session.inspect_recording(audio_path, state, language)
    return speech_view(state, audio)
''').body[0]
        assert ast.dump(function.body[1]) == ast.dump(expected_branch)
        function.body.pop(1)
        call = function.body[1].value
        expected = ast.parse('f(retain_audio=True)').body[0].value.keywords
        assert [ast.dump(k) for k in call.keywords] == [ast.dump(k) for k in expected]
        call.keywords = []
    elif function.name == "speech_view":
        additions = ast.parse('''
clip = state.get("stt_retry")
if clip:
    result[3] += (
        f"\\n\\nRetained WAV: {clip['sample_rate_hz']} Hz, {clip['channels']} channel(s), "
        f"{clip['sample_width_bytes'] * 8}-bit, {clip['duration_seconds']:.2f}s. "
        f"Language: {clip['language']}. Recording saved for retry."
    )
    if clip.get("inspection_only"):
        result[3] += (
            "\\nLocal inspection only: no API calls. "
            f"RMS: {clip['rms_fraction']}, peak: {clip['peak_fraction']}, "
            f"full-scale samples: {clip['full_scale_sample_fraction']}. "
            "Play/download the recording before choosing to transcribe it."
        )
result[5] = gr.update(
    value=clip["path"] if clip else None,
    interactive=state["mode"] in {"SCREEN", "DADI"} and not state.get("speech_paused"),
)
''').body
        assert [ast.dump(n) for n in function.body[-4:-1]] == [ast.dump(n) for n in additions]
        del function.body[-4:-1]
    return function


def without_brief_ui_additions(function):
    """D034 only: strip exact owner-brief UI additions for older behavior snapshots."""
    function = copy.deepcopy(function)
    snippets = {
        'speech_view': '''
if state.get("owner_brief") and state["mode"] == "DECIDE":
    result[3] += "\\n\\nCaller briefing (unverified): " + html.escape(
        state["owner_brief"]["spoken"]
    )
    if not state["owner_brief"]["acknowledged"]:
        result[3] += "\\n\\nListen to or read the briefing, then confirm to show your choices."
        result[4] = gr.update(visible=False)
''',
        'speech_choose': '''
if state.get("owner_brief") and not state["owner_brief"]["acknowledged"]:
    return speech_view(state)
''',
    }
    if function.name in snippets:
        index = 1 if function.name == 'speech_view' else 0
        expected = ast.parse(snippets[function.name]).body[0]
        assert ast.dump(function.body[index]) == ast.dump(expected)
        function.body.pop(index)
    if function.name in {'speech_turn', 'speech_retry_turn'}:
        call = next(n for n in ast.walk(function) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr in {'respond', 'retry'})
        assert call.keywords[-1].arg == 'owner_brief'
        assert ast.literal_eval(call.keywords[-1].value) is True
        call.keywords.pop()
    return function
