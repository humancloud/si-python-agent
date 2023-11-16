# StackInsights Python Agent


**StackInsights-Python**: The Python Agent for Apache StackInsights provides the native tracing/metrics/logging/profiling abilities for Python projects.

## Capabilities

| Reporter  | Supported?      | Details                                                    | 
|:----------|:----------------|:-----------------------------------------------------------|
| Trace     | ✅ (default: ON) | Automatic instrumentation + Manual SDK                     |            
| Log       | ✅ (default: ON) | Direct reporter only. (Tracing context in log planned)     |
| Meter     | ✅ (default: ON) | Meter API + Automatic PVM metrics                          |
| Profiling | ✅ (default: ON) | Threading and Greenlet Profiler                            |

## Installation Requirements

StackInsights Python Agent requires Python 3.7+.

> If you would like to try out the latest features that are not released yet, please refer to this [guide](docs/en/setup/faq/How-to-build-from-sources.md) to build from sources.
