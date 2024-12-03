package org.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedCondition;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class Prestashop {
    //Homepage
    @FindBy(id = "lnk-wszystkie-produkty")
    WebElement menuWszystkieProdukty;
    @FindBy(id = "category-66")
    WebElement menuMagic;
    @FindBy(id = "category-72")
    WebElement menuPokemon;
    @FindBy(xpath = "//*[@id=\"search_widget\"]/form/input[2]")
    WebElement searchInputField;
    @FindBy(id = "_desktop_cart")
    WebElement cart;


    //Categories page
    @FindBy(xpath = "//*[@id=\"left-column\"]/div[1]/ul/li[2]/ul/li[1]/a")
    WebElement submenuAkcesoria;
    @FindBy(xpath = "//*[@id=\"left-column\"]/div[1]/ul/li[2]/ul/li[2]/a")
    WebElement submenuGamesWorkshop;
    @FindBy(xpath = "//*[@id=\"left-column\"]/div[1]/ul/li[2]/ul/li[3]/a")
    WebElement submenuGryKarciane;
    @FindBy(xpath = "//*[@id=\"left-column\"]/div[1]/ul/li[2]/ul/li[4]/a")
    WebElement submenuPuzzle;

    //Product page
    @FindBy(xpath = "//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[2]/button")
    WebElement addToCartButton;
    @FindBy(id = "quantity_wanted")
    WebElement quantityWantedField;
    @FindBy(xpath = "//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[1]/div/span[3]/button[1]")
    WebElement quantityUpButton;
    @FindBy(xpath = "//*[@id=\"add-to-cart-or-refresh\"]/div[2]/div/div[1]/div/span[3]/button[2]")
    WebElement quantityDownButton;

    WebDriver driver;

    public Prestashop(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void openPage() {driver.get("https://localhost");}

    public void goBack() {driver.navigate().back();}

    public void waitForElement_byXpath(String xpath) {
        System.out.println("Waiting for element: " + xpath);
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.xpath(xpath)));
    }

    public void clickOn_menuWszystkieProdukty() {
        menuWszystkieProdukty.click();
        System.out.println("Go to menu Wszystkie Produkty");
    }

    public void clickOn_menuMagic() {
        menuMagic.click();
        System.out.println("Go to menu Magic the gathering");
    }

    public void clickOn_menuPokemon() {
        menuPokemon.click();
        System.out.println("Go to menu Pokemon");
    }

    public void clickOn_cart() {
        cart.click();
        System.out.println("Go to Cart");
    }

    public void clickOn_byXpath(String xpath) {
        waitForElement_byXpath(xpath);
        WebElement element = driver.findElement(By.xpath(xpath));
        element.click();
        System.out.println("Click element: " + xpath);
    }

    public boolean checkIfEnabled_addToCartButton() {
        if (addToCartButton.isEnabled()) {
            System.out.println("addToCartButton is enabled");
            return true;
        }
        else {
            System.out.println("addToCartButton is disabled");
            return false;
        }
    }

    public void clickOn_addToCartButton() {
        addToCartButton.click();
        System.out.println("Click addToCartButton");
    }

    public void clickOn_quantityUpButton() {
        quantityUpButton.click();
        System.out.println("Click quantityUpButton");
    }

    public boolean checkIfTextInsideElement_byXpath(String xpath, String text) {
        WebElement product = driver.findElement(By.xpath(xpath));

        String actualText = product.getText();
        if (actualText.contains(text)) {
            System.out.println("Text: " + text + " found in element: " + xpath);
            return true;
        }
        else {
            System.out.println("Text not found");
            return false;
        }
    }

    public void clearTextField_byId(String id) {
        driver.findElement(By.id(id)).clear();
        System.out.println("Text field: " + id + " was cleared");
    }

    public void inputTextField_byId(String id, String text) {
        clearTextField_byId(id);
        driver.findElement(By.id(id)).sendKeys(text);
        System.out.println("Text: " + text + " sent to text field: " + id);
    }

    public void search(String text) {
        searchInputField.clear();
        searchInputField.sendKeys(text);
        System.out.println("Searching for: " + text);
    }

    public void deleteProductFromCart_byXpath(String xpath) {
        WebElement element = driver.findElement(By.xpath(xpath));
        String deleteButtonXpath = xpath + "/div/div[3]/div/div[3]/div/a";
        clickOn_byXpath(deleteButtonXpath);
        System.out.println("Product: " + xpath + " deleted from cart");
    }

}
