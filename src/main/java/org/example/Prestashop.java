package org.example;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

public class Prestashop {
    @FindBy(linkText = "Pokémon")
    WebElement menuPokemon;
    @FindBy(linkText = "Magic the gathering")
    WebElement menuMagic;

    WebDriver driver;

    public Prestashop(WebDriver driver) {
        this.driver = driver;
        PageFactory.initElements(driver, this);
    }

    public void openPage() {driver.get("https://localhost");}
}
