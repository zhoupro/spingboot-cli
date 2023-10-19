package {{packageName}}.advice;


import {{packageName}}.exception.BizException;
import {{packageName}}.vo.Result;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;

@ControllerAdvice
public class GlobalExceptionAdvice {

    @ExceptionHandler({BizException.class})
    @ResponseBody
    public Result<Object> bizException(BizException exception) {
        return Result.failure(exception.getErrorCode(), exception.getErrorMsg());
    }

    @ExceptionHandler({RuntimeException.class})
    @ResponseBody
    public Result<Object> handleRuntimeException(RuntimeException exception) {
        return Result.failure(exception.getMessage());
    }
}


