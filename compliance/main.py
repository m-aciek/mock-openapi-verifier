from coverage.execfile import run_python_module


def run():
    import sys

    try:
        import respx
    except ImportError:
        pass
    else:
        old_get = respx.get
        old_patch = respx.patch

        def wrapped_get(*args, **kwargs):
            result = old_get(*args, **kwargs)
            old_mock = result.mock

            def wrapped_mock(*args, **kwargs):
                with open('.compliance', 'a') as meta:
                    meta.write(f'+get {kwargs}\n')
                return old_mock(*args, **kwargs)

            result.mock = wrapped_mock
            return result

        def wrapped_patch(*args, **kwargs):
            result = old_patch(*args, **kwargs)
            old_mock = result.mock

            def wrapped_mock(*args, **kwargs):
                with open('.compliance', 'a') as meta:
                    meta.write(f'+patch {kwargs}\n')
                return old_mock(*args, **kwargs)

            result.mock = wrapped_mock
            return result

        respx.get = wrapped_get
        respx.patch = wrapped_patch
    run_python_module(sys.argv[1:])
