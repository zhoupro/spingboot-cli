#!/usr/bin/env python3
""" 初始化 spring boot 项目。

Usage:
  sb.py  module create <module>
  sb.py  project create <groupId> <artifactId>
  sb.py  module delete <module>
"""

from docopt import docopt
import os
import xml.etree.ElementTree as ET
import shutil

ns = {'pom4': 'http://maven.apache.org/POM/4.0.0',
      'role': 'http://characters.example.com'}

sb_project = os.path.dirname(__file__)

def pretty_xml(element, indent, newline, level=0):  # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)

springboot2parent =  {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-parent",
            "version": "2.3.12.RELEASE",
        }


springboot2dependencyManage = [

    {
        "groupId": "org.springframework.cloud",
        "artifactId": "spring-cloud-dependencies",
        "version": "Hoxton.SR12",
        "type": "pom",
        "scope": "import"
    },

    {
        "groupId": "com.alibaba.cloud",
        "artifactId": "spring-cloud-alibaba-dependencies",
        "version": "2.2.6.RELEASE",
        "type": "pom",
        "scope": "import"
    },

    {
        "groupId": "org.projectlombok",
        "artifactId": "lombok",
        "version": "1.18.28"
    },

    {
        "groupId": "org.junit.jupiter",
        "artifactId": "junit-jupiter-api",
        "version": "5.3.1"
    },

    {
        "groupId": "org.springframework.boot",
        "artifactId": "mybatis-spring-boot-starter",
        "version": "3.0.1",
    },

    {
        "groupId": "com.baomidou",
        "artifactId": "mybatis-plus-boot-starter",
        "version": "3.5.3.1"
    },

    {
        "groupId": "com.alibaba",
        "artifactId": "druid-spring-boot-3-starter",
        "version": "1.2.18"
    },

    {
        "groupId": "org.mybatis",
        "artifactId": "mybatis",
        "version": "3.5.11"
    },

    {
        "groupId": "mysql",
        "artifactId": "mysql-connector-java",
        "version": "8.0.25"
    }

]

springboot2 = {

    "base": [
        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-test",
        },

        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-web",
        },

        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-aop",
        },

        {
            "groupId": "com.alibaba.cloud",
            "artifactId": "spring-cloud-starter-alibaba-nacos-discovery",
        },

        {
            "groupId": "com.alibaba.cloud",
            "artifactId": "spring-cloud-starter-alibaba-nacos-config",
        },


        {
            "groupId": "org.projectlombok",
            "artifactId": "lombok",
        },
    ],

    "mysql": [
        {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-jdbc",
        },
        {
            "groupId": "org.mybatis",
            "artifactId": "mybatis",
        },
        {
            "groupId": "com.alibaba",
            "artifactId": "druid-spring-boot-3-starter",
        },
        {
            "groupId": "mysql",
            "artifactId": "mysql-connector-java",
        }
    ],
    "kv": [
         {
            "groupId": "org.springframework.boot",
            "artifactId": "spring-boot-starter-data-redis",
        },
        {
            "groupId": "org.apache.commons",
            "artifactId": "commons-pool2",
        },
    ],

    "mq": [
        {
            "groupId": "org.springframework.kafka",
            "artifactId": "spring-kafka",
        }
    ]

}





def makeProject(groupId, artifactId):

    if not os.path.exists(artifactId):
        os.mkdir(artifactId)

    oldPwd = os.getcwd()
    os.chdir(artifactId)

    if not os.path.exists("./pom.xml"):
        shutil.copy(sb_project + "/temps/project-pom.xml", "./pom.xml")


    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    groupIdNode = root.find("{http://maven.apache.org/POM/4.0.0}groupId")
    groupIdNode.text = groupId
    artifactIdNode = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    artifactIdNode.text = artifactId

    parent = root.find("{http://maven.apache.org/POM/4.0.0}parent")

    if parent == None:
        # parent
        parent = ET.Element('parent')
        groupId = ET.SubElement(parent, 'groupId')
        groupId.text = springboot2parent.get("groupId")
        artifactId = ET.SubElement(parent, 'artifactId')
        artifactId.text = springboot2parent.get("artifactId")
        version = ET.SubElement(parent, 'version')
        version.text = springboot2parent.get("version")
        root.insert(5, parent)

    dependencyManagement = root.find("{http://maven.apache.org/POM/4.0.0}dependencyManagement")

    if dependencyManagement == None:
        #dependency
        dependencyManagement = ET.Element('dependencyManagement')
        dependencies = ET.SubElement(dependencyManagement, 'dependencies')
        for dep in springboot2dependencyManage:
            dependency = ET.SubElement(dependencies, 'dependency')
            groupId = ET.SubElement(dependency, 'groupId')
            groupId.text = dep.get("groupId")
            artifactId = ET.SubElement(dependency, 'artifactId')
            artifactId.text = dep.get("artifactId")
            version = ET.SubElement(dependency, 'version')
            version.text = dep.get("version")
            if dep.get("type", "") != "":
                type = ET.SubElement(dependency, 'type')
                type.text = dep.get("type")
            if dep.get("scope", "") != "":
                scope = ET.SubElement(dependency, 'scope')
                scope.text = dep.get("scope")

        if len(springboot2dependencyManage) > 0 :
            root.insert(5, dependencyManagement)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)
    os.chdir(oldPwd)


def getProjectInfo(pomxml):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pomxml)
    root = tree.getroot()
    version = root.find("{http://maven.apache.org/POM/4.0.0}version")
    groupId = root.find("{http://maven.apache.org/POM/4.0.0}groupId")
    artifactId = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    # 获取项目信息
    return {

        "version": version.text,
        "groupId": groupId.text,
        "artifactId": artifactId.text
    }

def isProject(pomxml):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pomxml)
    root = tree.getroot()
    packaging = root.find("{http://maven.apache.org/POM/4.0.0}packaging")
    return packaging != None and packaging.text == "pom"

def addModuleToProject(moduleName,pwd):
    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse(pwd+"/pom.xml")
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    modules = root.find("{http://maven.apache.org/POM/4.0.0}modules")
    if modules == None:
        parent = ET.Element('modules')
        groupId = ET.SubElement(parent, 'module')
        groupId.text = moduleName
        root.insert(5, parent )
    else:
        findFlag = False
        for m in modules:
            if m.text == moduleName:
                print("exist module")
                findFlag = True
                break
        if findFlag == False:
            module = ET.Element('module')
            module.text = moduleName
            modules.append(module)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)



def makeModule( artifactId, pwd ):
    if  os.path.exists(pwd + "/" + artifactId) :
        print(" module exist")
        return

    if not isProject(pwd+"/pom.xml"):
        print("current dir is not project")
        return

    addModuleToProject(artifactId, pwd)

    targetPath = pwd + "/" +artifactId
    if not os.path.exists(targetPath):
        os.mkdir(targetPath)
    oldPwd = pwd
    os.chdir(artifactId)
    if not os.path.exists("./pom.xml"):
        shutil.copy(sb_project+ "/temps/module-pom.xml", "./pom.xml")

    parentInfo = getProjectInfo("../pom.xml")
    parentGroupId = parentInfo.get("groupId")
    parentArtifactId = parentInfo.get("artifactId")
    parentVersion = parentInfo.get("version")

    import xml.etree.ElementTree as ET
    # 加载POM文件
    tree = ET.parse('pom.xml')
    ns = "http://maven.apache.org/POM/4.0.0"
    ET.register_namespace('', ns)
    root = tree.getroot()
    artifactIdNode = root.find("{http://maven.apache.org/POM/4.0.0}artifactId")
    artifactIdNode.text = artifactId

    parentNode = root.find("{http://maven.apache.org/POM/4.0.0}parent")
    if parentNode == None:
        parent = ET.Element('parent')
        groupId = ET.SubElement(parent, 'groupId')
        groupId.text = parentGroupId
        artifactId = ET.SubElement(parent, 'artifactId')
        artifactId.text = parentArtifactId
        version = ET.SubElement(parent, 'version')
        version.text = parentVersion
        root.insert(2, parent)

    pretty_xml(root, '\t', '\n')
    tree.write('pom.xml', encoding="utf-8", xml_declaration=True)
    os.chdir(oldPwd)






if __name__ == '__main__':
    arguments = docopt(__doc__.format(filename=os.path.basename(__file__)))

    cmd_root = os.getcwd()

    if arguments.get("module"):
        if arguments.get("create"):
            makeModule(arguments.get("<module>"), cmd_root)

    if arguments.get("project"):
        if arguments.get("create"):
            makeProject(arguments.get("<groupId>"), arguments.get("<artifactId>"))



    # os.chdir("springboot1")
    # makeModule("common")
    # os.chdir("springboot1")
    # getProjectInfo()
    # addSpringBootParent()





# 1, 创建 module

# 2, 删除 module

# 3, 重命名 module

# 4, module 新增依赖，同步新增到父项目。如果父项目已经声明依赖，则只新增子项目依赖。

# 5，列出项目已使用依赖
# 6，列出项目已声明的依赖



