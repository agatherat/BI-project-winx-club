import org.example.Prestashop;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import testbase.TestBase;

public class PrestashopTestset extends TestBase {
    static Prestashop pagePrestashop = new Prestashop(driver);

    @Test
    public void testAddProductsToCart() {
        pagePrestashop.openPage();

    }
}
