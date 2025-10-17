from fastapi.responses import JSONResponse


def page(a: int, b: int) -> JSONResponse:
    return JSONResponse({"add": {"a": a, "b": b}, "result": a + b})
