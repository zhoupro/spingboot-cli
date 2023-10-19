package {{packageName}}.exception;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BizException extends RuntimeException{
    protected Integer errorCode;
    protected String errorMsg;

}
