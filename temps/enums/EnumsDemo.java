package {{packageName}}.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;
import java.util.Arrays;

@Getter
@AllArgsConstructor
public enum EnumsDemo {
    YES("ok", "确定"),
    NO("no","取消"),
    ;

    private String code;
    private String desc;

    /**
     * 通过code获取desc
     *
     * @param code code
     * @return desc
     */
    public static String descOfCode(String code) {
        return Arrays.stream(values())
                .filter(it -> it.getCode().equals(code))
                .findFirst()
                .map(a -> a.desc)
                .orElse(null);
    }

}
