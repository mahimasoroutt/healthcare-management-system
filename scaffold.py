import os

base_dir = "hms"
src_main_java = os.path.join(base_dir, "src", "main", "java", "com", "hospital", "hms")
src_main_resources = os.path.join(base_dir, "src", "main", "resources")
templates = os.path.join(src_main_resources, "templates")
static = os.path.join(src_main_resources, "static")
css = os.path.join(static, "css")
js = os.path.join(static, "js")
src_test_java = os.path.join(base_dir, "src", "test", "java", "com", "hospital", "hms")

directories = [
    src_main_java,
    os.path.join(src_main_java, "config"),
    os.path.join(src_main_java, "controller"),
    os.path.join(src_main_java, "dto"),
    os.path.join(src_main_java, "entity"),
    os.path.join(src_main_java, "repository"),
    os.path.join(src_main_java, "service"),
    os.path.join(src_main_java, "security"),
    os.path.join(src_main_java, "exception"),
    src_main_resources,
    templates,
    os.path.join(templates, "admin"),
    os.path.join(templates, "doctor"),
    os.path.join(templates, "patient"),
    os.path.join(templates, "auth"),
    os.path.join(templates, "fragments"),
    static,
    css,
    js,
    src_test_java
]

for d in directories:
    os.makedirs(d, exist_ok=True)

# Create Main Class
main_class = """package com.hospital.hms;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class HmsApplication {

	public static void main(String[] args) {
		SpringApplication.run(HmsApplication.class, args);
	}

}
"""
with open(os.path.join(src_main_java, "HmsApplication.java"), "w") as f:
    f.write(main_class)

# Create application.properties
app_props = """spring.application.name=hms

spring.datasource.url=jdbc:mysql://localhost:3306/hospital_managment?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC
spring.datasource.username=${DB_USERNAME:root}
spring.datasource.password=${DB_PASSWORD:root}
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQLDialect

spring.thymeleaf.cache=false
"""
with open(os.path.join(src_main_resources, "application.properties"), "w") as f:
    f.write(app_props)

print("Scaffolding complete.")
