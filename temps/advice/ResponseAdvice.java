package {{packageName}}.advice;

import brave.Tracer;
import {{packageName}}.enums.ResultCode;
import {{packageName}}.vo.Result;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.SneakyThrows;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.MethodParameter;
import org.springframework.http.MediaType;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.server.ServerHttpRequest;
import org.springframework.http.server.ServerHttpResponse;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseBodyAdvice;

@RestControllerAdvice(basePackages = {"{{packageName}}"})
public class ResponseAdvice  implements ResponseBodyAdvice<Object> {

    @Autowired
    ObjectMapper objectMapper;


    @Autowired
    private Tracer tracer;

    @Override
    public boolean supports(MethodParameter returnType, Class<? extends HttpMessageConverter<?>> converterType) {
        return ! returnType.hasMethodAnnotation(NotControllerResponseAdvice.class);
    }

    @SneakyThrows
    @Override
    public Object beforeBodyWrite(Object body, MethodParameter returnType, MediaType selectedContentType, Class<? extends HttpMessageConverter<?>> selectedConverterType, ServerHttpRequest request, ServerHttpResponse response)  {

        String s = tracer.currentSpan().context().traceIdString();
        if (body instanceof Result){
            ((Result<?>) body).setTraceId(s);
            return body;
        }

        if (body instanceof  String){
            Result<Object> success = Result.success(ResultCode.RC100.getMessage(), body);
            success.setTraceId(s);
            return objectMapper.writeValueAsString(success);
        }
        Result<Object> success = Result.success(ResultCode.RC100.getMessage(), body);
        success.setTraceId(s);
        return success;
    }

}