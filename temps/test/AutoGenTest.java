package {{packageName}}.autogen;

import com.baomidou.mybatisplus.generator.FastAutoGenerator;
import org.assertj.core.util.Lists;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;


@SpringBootTest
public class AutoGenTest {


    @Value("${spring.datasource.url}")
    private String url ;
    @Value("${spring.datasource.username}")
    private String userName ;
    @Value("${spring.datasource.password}")
    private String password;
    @Test
    void Gen(){
        List<String> tables = Lists.newArrayList(
                "t_sample",
//                "t_sample1",
                "t_sample2"
        );



        FastAutoGenerator.create(url, userName,password)
                .globalConfig(builder -> {
                    builder.author("authorName") // 设置作者
                            .outputDir("./src/output/autogen"); // 指定输出目录
                })
                .packageConfig(builder -> {
                    builder.parent("{{packageName}}") ;// 设置父包名

                })
                .strategyConfig(builder -> {
                    builder.addInclude(tables);
                })
                .execute();
    }
}
