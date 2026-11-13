"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    scores = {'sequential': 1, 'fan_out_fan_in': 1 + 3 * data['needs_parallel'],
              'evaluator_optimizer': 1 + 3 * data['needs_review'], 'blackboard': 1 + 3 * data['needs_shared_state']}
    selected = sorted(scores, key=lambda name: (-scores[name], name))[:2]
    rationale = await agent.ask('architect', 'Explain the selected patterns, one cost trade-off, and when a simpler design suffices.',
        {'constraints': data, 'scores': scores, 'selected': selected}, 'Combine parallel evidence collection with a bounded review stage; each extra model call adds cost.')
    return {'scores': scores, 'selected': selected, 'rationale': rationale}
