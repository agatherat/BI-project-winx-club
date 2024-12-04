package testbase;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

public class TestBase {
    static String driverPath = System.getenv("chromeDriver");
    public static WebDriver driver;

    @BeforeAll
    public static void initializeWebDriver() {
        System.setProperty("webdriver.chrome.driver", ".\\drivers\\chromedriver-win64\\chromedriver.exe");
        //options
        driver = new ChromeDriver();
        driver.manage().window().maximize();
    }

    @AfterAll
    public static void quitDriver() {driver.quit();}
}
