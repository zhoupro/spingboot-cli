package {{packageName}}.autogen;

import com.baomidou.mybatisplus.generator.FastAutoGenerator;
import com.baomidou.mybatisplus.generator.config.OutputFile;
import com.github.davidfantasy.mybatisplus.generatorui.GeneratorConfig;
import com.github.davidfantasy.mybatisplus.generatorui.MybatisPlusToolsApplication;
import org.assertj.core.util.Lists;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Collections;
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
                "t_sample1",
                "t_sample2"
        );



        FastAutoGenerator.create(url, userName,password)
                .globalConfig(builder -> {
                    builder.author("authorName") // 设置作者
                            .outputDir("./src/main/java"); // 指定输出目录
                })
                .packageConfig(builder -> {
                    builder.parent("{{packageName}}")
                            .entity("model.entity") //设置entity包名
                            .controller("controller")
                            .mapper("model.mapper")
                            .service("model.service")
                            .serviceImpl("model.service.impl")
                            .pathInfo(Collections.singletonMap(OutputFile.xml, "./src/main/resources/mapper"));
                })
                .strategyConfig(builder -> {
                    builder.addInclude(tables);
                })
                .execute();
    }


    @Test
    void AutoGenUI() throws InterruptedException {

        GeneratorConfig config = GeneratorConfig.builder().jdbcUrl(url)
                .userName(userName)
                .password(password)
                .driverClassName("com.mysql.cj.jdbc.Driver")
                .basePackage("{{packageName}}")
                .port(8068)
                .build();
        MybatisPlusToolsApplication.run(config);
        // 防止Server 退出
        Thread.sleep(10000000000L);
    }
}