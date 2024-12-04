import org.example.Prestashop;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.junit.jupiter.api.MethodOrderer.OrderAnnotation;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.AfterTest;
import testbase.TestBase;

import static java.lang.Thread.activeCount;
import static java.lang.Thread.sleep;

@TestMethodOrder(OrderAnnotation.class)
public class PrestashopTestset extends TestBase {
    static Prestashop pagePrestashop = new Prestashop(driver);

    @Test
    @Order(1)
    public void test_addProductsToCart() throws InterruptedException {
        pagePrestashop.openPage();

        String[] categories = {"Magic", "Pokemon"};
        String page = "";

        for (String cat : categories) {
            if (cat.equals("Magic")) {
                pagePrestashop.clickOn_menuMagic();
                page = "https://localhost/66-magic-the-gathering";
            }
            else if (cat.equals("Pokemon")) {
                pagePrestashop.clickOn_menuPokemon();
                page = "https://localhost/72-pokemon";
            }

            pagePrestashop.addProductsToCart(page,5);
        }
    }

    @Test
    @Order(2)
    public void test_searchForProductsAndAddToCart() throws InterruptedException {
        pagePrestashop.openPage();
        pagePrestashop.clickOn_menuWszystkieProdukty();

        pagePrestashop.search("lorcana\n");
        pagePrestashop.addProductsToCart("https://localhost/szukaj?controller=search&s=lorcana",1);
    }

    @Test
    @Order(3)
    public void test_deleteProductsFromCart() {
        pagePrestashop.openPage();

//        pagePrestashop.goToPage("https://localhost/69-one-piece");
//        pagePrestashop.addProductsToCart("https://localhost/69-one-piece", 3);

        pagePrestashop.clickOn_cart();

        for (int j = 1; j < 4; j++)
            pagePrestashop.deleteProductFromCart_byXpath("//*[@id=\"main\"]/div/div[1]/div/div[2]/ul/li[" + j + "]");
    }

    @Test
    @Order(4)
    public void test_registerNewAccount() {
        pagePrestashop.openPage();
        pagePrestashop.clickOn_logIn();

        pagePrestashop.clickOn_byXpath("//*[@id=\"content\"]/div/a");   //click on registration link

        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[1]/div[1]/label[2]/span");   //select gender radiobox
        pagePrestashop.inputTextField_byId("field-firstname", "test-name");
        pagePrestashop.inputTextField_byId("field-lastname", "test-surname");
        pagePrestashop.inputTextField_byId("field-email", "email@test");
        pagePrestashop.inputTextField_byId("field-password", "password");

        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[8]/div[1]/span");    //select checkbox
        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[10]/div[1]/span");   //select checkbox

        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/footer/button"); //click on submit button
    }

    @Test
    @Order(5)
    public void test_createOrder() {
        pagePrestashop.openPage();

//        pagePrestashop.goToPage("https://localhost/74-star-wars-unlimited");
//        pagePrestashop.addProductsToCart("https://localhost/74-star-wars-unlimited", 1);

        pagePrestashop.clickOn_cart();

        pagePrestashop.clickOn_byXpath("//*[@id=\"main\"]/div/div[2]/div/div[2]/div");    //click on button "Przejdź do realzacji zamówień"

//        pagePrestashop.clickOn_byXpath("//*[@id=\"checkout-personal-information-step\"]/div/ul/li[3]/a"); //click on login
//        pagePrestashop.inputTextField_byId("field-email", "newemail@test");
//        pagePrestashop.inputTextField_byId("field-password", "password");
//        pagePrestashop.clickOn_byXpath("//*[@id=\"login-form\"]/footer/button");    //click on login button


//        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[1]/div[1]/label[2]/span");   //select gender radiobox
//        pagePrestashop.inputTextField_byId("field-firstname", "test-name");
//        pagePrestashop.inputTextField_byId("field-lastname", "test-surname");
//        pagePrestashop.inputTextField_byId("field-email", "new-email@test");
//        pagePrestashop.inputTextField_byId("field-password", "password");
//
//        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[8]/div[1]/span");    //select checkbox
//        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/div/div[10]/div[1]/span");   //select checkbox
//
//        pagePrestashop.clickOn_byXpath("//*[@id=\"customer-form\"]/footer/button"); //click on personal data submit button

        pagePrestashop.inputTextField_byId("field-address1", "test-address");
        pagePrestashop.inputTextField_byId("field-postcode", "12-345");
        pagePrestashop.inputTextField_byId("field-city", "test-city");

        pagePrestashop.clickOn_byXpath("//*[@id=\"delivery-address\"]/div/footer/button");  //click on address submit button

        pagePrestashop.clickOn_byId("delivery_option_7");
        pagePrestashop.clickOn_byXpath("//*[@id=\"js-delivery\"]/button");  //click on delivery submit button

        pagePrestashop.clickOn_byId("payment-option-2"); //select payment radiobutton
        pagePrestashop.clickOn_byXpath("/html/body/main/section/div/div/section/div/div[1]/section[4]/div/form/ul/li/div[1]/span/input");

        pagePrestashop.clickOn_byXpath("//*[@id=\"payment-confirmation\"]/div[1]/button");  //click on order submit button
    }

    @Test
    @Order(6)
    public void test_checkOrderStatus() {
        pagePrestashop.openPage();

        pagePrestashop.clickOn_byXpath("//*[@id=\"footer_account_list\"]/li[2]/a"); //click on orders link
        pagePrestashop.clickOn_byXpath("//*[@id=\"content\"]/table/tbody/tr[1]/td[6]/a[1]");    //click on order details link
        System.out.println("Order Status: " + pagePrestashop.getElementText_byXpath("//*[@id=\"order-history\"]/table/tbody/tr/td[2]/span"));
    }

    @Test
    @Order(7)
    public void test_downloadInvoice() throws InterruptedException {
        //change order status in admin panel
        pagePrestashop.goToPage("https://localhost:/admin4577/");
        pagePrestashop.clickOn_byXpath("//*[@id=\"subtab-AdminParentOrders\"]/a"); //click on "Zamówienia" menu
        pagePrestashop.clickOn_byXpath("//*[@id=\"subtab-AdminOrders\"]/a");    //click on "Zamówienia" submenu
        pagePrestashop.clickOn_byXpath("//*[@id=\"order_grid_table\"]/tbody/tr[1]/td[9]/div/button");   //click on toggle
        pagePrestashop.clickOn_byXpath("//*[@id=\"order_grid_table\"]/tbody/tr[1]/td[9]/div/div/button[12]"); //click on "Płatność przyjęta" option

        sleep(3000);

        pagePrestashop.openPage();
        pagePrestashop.clickOn_byXpath("//*[@id=\"footer_account_list\"]/li[2]/a"); //click on orders link
        pagePrestashop.clickOn_byXpath("//*[@id=\"content\"]/table/tbody/tr[1]/td[5]/a");   //click on invoice link
    }
}

