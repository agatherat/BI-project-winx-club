import org.example.Prestashop;
import org.junit.jupiter.api.Test;
import testbase.TestBase;


public class PrestashopTestset extends TestBase {
    static Prestashop pagePrestashop = new Prestashop(driver);

    @Test
    public void test_addProductsToCart() {
        pagePrestashop.openPage();

        String[] categories = {"Magic", "Pokemon"};
        Integer[] quantities = {1, 2, 3, 4, 5};
        int count = 0;
        int i = 1;

        for (String cat : categories) {
            if (cat.equals("Magic"))
                pagePrestashop.clickOn_menuMagic();
            else if (cat.equals("Pokemon"))
                pagePrestashop.clickOn_menuPokemon();

            while (count < 5) {
                String productXpath = "//*[@id=\"js-product-list\"]/div[1]/div[" + i + "]";

                pagePrestashop.clickOn_byXpath(productXpath);

                if (pagePrestashop.checkIfEnabled_addToCartButton()) {
                    for (int j = 0; j < quantities[i % quantities.length] - 1; j++)
                        pagePrestashop.clickOn_quantityUpButton();
                    pagePrestashop.clickOn_addToCartButton();

                    if(!pagePrestashop.checkIfEnabled_addToCartButton()) {
                        pagePrestashop.clearTextField_byId("quantity_wanted");
                        pagePrestashop.clickOn_addToCartButton();
                    }

                    count++;
                }

                pagePrestashop.goBack();
                i++;
            }

            count = 0;
            i = 1;
        }
    }

    @Test
    public void test_searchForProductsAndAddToCart() {
        pagePrestashop.openPage();
        pagePrestashop.clickOn_menuWszystkieProdukty();

        pagePrestashop.search("Magic");

        int count = 0;
        int i = 1;

        while (count < 1) {
            String productXpath = "//*[@id=\"js-product-list\"]/div[1]/div[" + i + "]";

            pagePrestashop.clickOn_byXpath(productXpath);

            if (pagePrestashop.checkIfEnabled_addToCartButton()) {
                pagePrestashop.clickOn_addToCartButton();

                count++;
            }

            pagePrestashop.goBack();
            i++;
        }
    }

    @Test
    public void test_deleteProductsFromCart() {
        pagePrestashop.openPage();
        pagePrestashop.clickOn_menuWszystkieProdukty();

        int count = 0;
        int i = 1;

        while (count < 3) {
            String productXpath = "//*[@id=\"js-product-list\"]/div[1]/div[" + i + "]";

            pagePrestashop.clickOn_byXpath(productXpath);

            if (pagePrestashop.checkIfEnabled_addToCartButton()) {
                pagePrestashop.clickOn_addToCartButton();
                count++;
            }

            pagePrestashop.goBack();
            i++;
        }

        pagePrestashop.clickOn_cart();

        for (int j = 1; j < 4; j++)
            pagePrestashop.deleteProductFromCart_byXpath("//*[@id=\"main\"]/div/div[1]/div/div[2]/ul/li[" + j + "]");
    }
}

