import random
import string
import time

import selenium.common.exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import logging
from . import BasicAlgorithm
from .exceptions import AlgorithmExecutingError, TwitterBotWarning
from utils.bot_humanity import random_sleep, simulate_input_in_element

logger = logging.getLogger(__name__)


class GetChatsAlgorithm(BasicAlgorithm[list]):
    """
    In result returns list of parsed chats links.
    """

    #logger.debug("GetChatsAlgorithm created")

    def start(self) -> list:
        return ['https://x.com/messages/1804212233028677845', 'https://x.com/messages/1805186246467092643',
                'https://x.com/messages/1734577014873661634', 'https://x.com/messages/1734226282299207771']
        #logger.debug("GetChatsAlgorithm started")
        """
        Parse chat links from the Twitter messages page.
        """
        chat_links = []

        #self.#logger.debug("initializing driver")

        # make window active
        self.driver.switch_to.window(self.driver.current_window_handle)

        # Open the Twitter messages page and parse chat links twice
        for _ in range(2):
            self.driver.get("https://x.com/messages")
            #self.#logger.debug("opening twitter messages page")
            self.driver.execute_script("document.body.style.zoom = '35%'")
            #logger.debug("zooming")

            # wait for message will be present on page
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//main[@role='main']"))
            )

            #self.#logger.debug("scrolling down")
            time.sleep(random.randint(5, 20))
            self.driver.vertical_scroller.scroll_to(300)

            #self.#logger.debug("searching chat links")

            i = 0
            last_height = self.driver.vertical_scroller.max_scroll_y
            #logger.debug("last height: " + str(last_height))
            while True:
                #logger.debug("iteration: " + str(i))
                count = 0
                #logger.debug("searching chat links")
                time.sleep(random.randint(5, 20))

                """
                SEARCH
                """
                try:
                    link_elements = self.driver.find_elements(
                        By.XPATH, '//div[@data-testid="conversation"]//a[1]'
                    )
                    #logger.debug("try to find chat links")
                    for _ in range(3):
                        for link_element in link_elements:
                            #logger.debug("found chat link")
                            """
                            GET ONLY CHAT LINKS
                            """
                            link = link_element.get_attribute("href").replace(
                                "/participants", ""
                            )
                            #logger.debug(link)
                            if "https://x.com/messages/" or "https://twitter.com/messages" in link:
                                #logger.debug("is chat link")
                                chat_id = link.replace(
                                    "https://x.com/messages/", ""
                                ).replace("https://twitter.com/messages/", "")
                                #logger.debug(chat_id)
                                chat_id.replace("-", "")
                                #logger.debug("replaced in chat id")

                                """
                                CHECK IS CHAT LINK VALID AND LINK NOT IN chat_links_total
                                """
                                if all(char.isdigit() for char in chat_id) and not (
                                        link in chat_links
                                ):
                                    #logger.debug("is valid chat link")
                                    chat_links.append(link)
                                    logger.debug(f"added chat link {link}")
                                    count += 1

                                #logger.debug(f"added chat links count: {count}")

                    #self.#logger.debug(f"added chat links count: {count}")

                except Exception as error:
                    self.logger.warning(f"failed parse chat links, try again: {error}")
                    continue

                """
                SCROLL
                """
                self.driver.vertical_scroller.scroll_to(
                    self.driver.vertical_scroller.current_scroll_y + 1000
                )
                #logger.debug("scrolled")

                time.sleep(10)

                new_height = self.driver.vertical_scroller.max_scroll_y
                #logger.debug("new height: " + str(new_height))

                if new_height == last_height:
                    if i == 3:
                        #logger.debug("failed parse chat links")
                        break
                    else:
                        #logger.debug("try again")
                        i += 1
                        continue

                last_height = new_height

        self.driver.execute_script("document.body.style.zoom = '100%'")
        #logger.debug("zoomed")
        return chat_links


class SendGIFAlgorithm(BasicAlgorithm[None]):
    """
    Send a GIF in the opened chat.
    Needs a kwarg: message_text
    """

    def start(self, message_text: str = None) -> None:
        #self.#logger.debug("sending GIF to the chat")

        # click on `add a gif` button
        possible_aria_labels = [
            "Add a GIF",
            "Добавить GIF-файл",
            "Додати GIF-файл",
            "Tambahkan GIF",
        ]
        #logger.debug("possible_aria_label init")
        for i, aria_label in enumerate(possible_aria_labels):
            #logger.debug("loop of possible_aria_labels")
            try:
                #logger.debug(f"trying to click on {aria_label}")
                timeout = 12 if i == 0 else 1  # first time wait for page loading
                WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f'//button[@aria-label="{aria_label}"]',
                        )
                    )
                ).click()
                #self.#logger.debug(f"successful click on {aria_label}")
                break
            except:
                self.logger.warning(f"failed click on {aria_label}")
                continue

        # write random gif name chars
        try:
            #self.#logger.debug("entering gif name")
            random_letters = "".join(
                random.choice(string.ascii_letters) for _ in range(random.randint(1, 5))
            )
            #self.#logger.debug(f"random letters: {random_letters}")
            simulate_input_in_element(
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "input"))
                ),
                random_letters,
            )
            #self.#logger.debug(f"successful entered gif name: {random_letters}")
        except Exception as error:
            self.logger.warning(f"failed to enter gif name")
        random_sleep()
        #logger.debug("random sleep")

        # find and click on search button
        try:
            WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[.//span[contains(text(), "Search")]]')
                )
            ).click()
            #self.#logger.debug(f"successful search button")
        except Exception as error:
            pass

        # select gif
        try:
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@data-testid="gifSearchGifImage"]')
                )
            ).click()
            #self.#logger.debug(f"successful selected gif")
        except Exception as error:
            raise AlgorithmExecutingError(f"failed to select gif: {error}")

        # enter message text
        random_sleep()
        #logger.debug("random sleep")
        try:
            #self.#logger.debug("entering message text")
            if message_text:
                #self.#logger.debug(f"message text: {message_text}")
                message_text = message_text.decode('utf-8')
                #logger.debug(f"message text: {message_text}")
                WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//*[@data-testid" "='dmComposerTextInput']")
                    )
                ).click()
                #logger.debug("clicked on input field")
                input_field = self.driver.find_element(
                    By.XPATH, "//*[@data-testid='dmComposerTextInput']"
                )
                #logger.debug("found input field")
                message_text = message_text.replace("'", '')
                self.driver.execute_script(
                    f"""const textarea = arguments[0];
                                                    const text = `{message_text}`;

                                                    textarea.addEventListener('paste', function(event) {{
                                                      event.preventDefault();
                                                      document.execCommand('insertText', false, text);
                                                    }});

                                                    const clipboardEvent = new ClipboardEvent('paste', {{
                                                      clipboardData: new DataTransfer()
                                                    }});

                                                    clipboardEvent.clipboardData.setData('text/plain', text);

                                                    textarea.dispatchEvent(clipboardEvent);
                                                        """,
                    input_field,
                )
                #logger.debug("pasted message text")

                #self.#logger.debug(f"successful enter message text: {message_text}")
            else:
                ...
                #self.#logger.debug(f"there is no message text")
        except Exception as error:
            self.logger.warning(f"failed to enter message text:\n{error}")

        # press send key
        random_sleep()
        #logger.debug("random sleep")
        try:
            #self.#logger.debug("pressing send key")
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[@data-testid="dmComposerSendButton"]')
                )
            ).click()
            #logger.debug("pressed send key")
        except Exception as error:
            raise AlgorithmExecutingError(f"failed to press send gif: {error}")

        # check if gif send successful
        random_sleep()
        #logger.debug("random sleep")
        try:
            for i in range(
                    20
            ):
                #logger.debug("searching gif in attachments")
                # if we found gif in attachments after 20 seconds == gif not sent
                WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "[data-testid=dmComposerAttachments]")
                    )
                )
                #logger.debug("found gif in attachments")
                time.sleep(1)

            #self.#logger.debug("gif send successful")

            raise AlgorithmExecutingError(f"failed send to chat")

        except selenium.common.exceptions.TimeoutException:
            ...  #self.#logger.debug(f"successful send to chat")

        except Exception as error:
            raise AlgorithmExecutingError(f"{error}")


class RetweetProfileMediaAlgorithm(BasicAlgorithm[int]):
    #logger.debug("RetweetProfileMediaAlgorithm init")
    """
    In result returns count of success retweets
    """

    def start(self) -> int:
        retweet_count = 0
        try:
            time.sleep(5)
            sensitive_content_confirm_button = self.driver.find_element(By.XPATH, '//button[.//span[text()="Yes, view '
                                                                                  'profile"]]')
            time.sleep(2)
            sensitive_content_confirm_button.click()
            time.sleep(2)
            print("sensitive_content_confirm_button found")
        except:
            pass
        #logger.debug("RetweetProfileMediaAlgorithm start")

        self.close_popup_if_exist()
        #logger.debug("close popup if exist")

        # scroll page down
        self.driver.vertical_scroller.scroll_to(500)
        #logger.debug("scroll page down")
        pinned = None
        try:
            pinned = self.driver.find_element(By.XPATH,
                                              "//div[@data-testid='socialContext' and contains(text(), 'Pinned')]")
        except:
            logger.debug("pinned not found")
        # if pinned we use other algorithm  
        if pinned:
            retweet_count = self.__do_retweet_pinned()

            return retweet_count
        # search media content
        try:
            media_group = self.driver.find_elements(By.XPATH, "//li[@role='listitem']")
            #self.#logger.debug(f"found {len(media_group)} media")
        except:
            raise AlgorithmExecutingError("media not found")

        baned_text = "Age-restricted adult content"
        # if baned_text in self.driver.page_source then warning
        if baned_text in self.driver.page_source:
            raise TwitterBotWarning(f"{baned_text}. Please add your age to account settings.")

        if media_group:
            #logger.debug("media found")
            try:
                #logger.debug("click on media")
                try:
                    #logger.debug("click on media")
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//li[@role="listitem"]//button',
                            )
                        )
                    ).click()
                    self.driver.execute_script("""
                        document.evaluate(
                          '//li[@role="listitem"]//button', 
                          document, 
                          null, 
                          XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, 
                          null
                        ).snapshotItem(1).click();"""
                                               )
                    #logger.debug("clicked on media")
                except selenium.common.exceptions.TimeoutException:
                    logger.debug("Sensitive content on media was not found. Retweeting media..")
                except Exception as ex:  # might can`t be clicked
                    logger.exception("Failed to click sensitive content on media. Might be: element is not clickable\n"
                                     f"Media element: {media_group[0]}\n")

                try:
                    #logger.debug("click on media")
                    media = media_group[0]
                    media.click()
                    #logger.debug("clicked on media")
                except:
                    pass
                try:
                    #logger.debug("click on media")
                    media = media_group[0]
                    media.click()
                    #logger.debug("clicked on media")
                except:
                    pass
                random_sleep(1, 3)
                #logger.debug("random sleep")
                self.driver.switch_to.window(self.driver.current_window_handle)
                #logger.debug("switch to window")
                # make repost if first time
                try:
                    #logger.debug("make repost if first time (1)")
                    self.__do_retweet_media_element()
                    #logger.debug("make repost if first time (2)")
                    #self.#logger.debug(f"successful retweet media first time")
                    retweet_count += 1
                    #logger.debug("make repost if first time")
                except Exception as error:
                    try:
                        #logger.debug("make repost if first time")
                        # make undo repost
                        # click on button to show side_menu for unretweet
                        WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//button[@data-testid='unretweet']")
                            )
                        )
                        #logger.debug("make undo repost")
                        element = self.driver.find_element(
                            By.XPATH, "//button[@data-testid='unretweet']"
                        )
                        #logger.debug("click on button to show side_menu for unretweet")
                        self.driver.execute_script("arguments[0].click()", element)
                        #logger.debug("clicked on button to show side_menu for unretweet")
                        # click on button to unretweet confirm
                        WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//div[@data-testid='unretweetConfirm']")
                            )
                        )
                        #logger.debug("click on button to unretweet confirm")
                        element = self.driver.find_element(
                            By.XPATH, "//div[@data-testid='unretweetConfirm']"
                        )
                        #logger.debug("click on button to unretweet confirm")
                        self.driver.execute_script("arguments[0].click()", element)
                        #logger.debug("clicked on button to unretweet confirm")
                        random_sleep(1, 3)
                        #logger.debug("random sleep")

                        self.__do_retweet_media_element()
                        #self.#logger.debug(f"successful retweet media again")
                        retweet_count += 1
                        #logger.debug("make undo repost")
                    except Exception as error:
                        raise AlgorithmExecutingError(
                            f"error during retweet again: {error}"
                        )
            except Exception as error:
                raise AlgorithmExecutingError(f"Error during repost media: {error}")
        else:
            raise AlgorithmExecutingError(f"media not found on page")

        #self.#logger.debug(f"Retweeted {retweet_count} tweets")
        return retweet_count

    def __do_retweet_media_element(self):
        #logger.debug("make repost if first time")
        # click on button to show side_menu for repost
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='retweet']"))
        )
        #logger.debug("get button to show side_menu for repost")
        element = self.driver.find_element(By.XPATH, "//button[@data-testid='retweet']")
        #logger.debug("click on button to show side_menu for repost")
        self.driver.execute_script("arguments[0].click()", element)
        # click on button repost
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//div[@data-testid="retweetConfirm"]')
            )
        )
        #logger.debug("click on button repost")
        element = self.driver.find_element(
            By.XPATH, '//div[@data-testid="retweetConfirm"]'
        )
        #logger.debug("click on button repost")
        self.driver.execute_script("arguments[0].click()", element)
        logger

    def close_popup_if_exist(self):
        try:
            #self.#logger.debug("close alert popup about content")
            self.driver.switch_to.window(self.driver.current_window_handle)
            #self.#logger.debug("switch to window")
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@role='button' and @data-testid='empty_state_button_text']",
                    )
                )
            ).click()
            #self.#logger.debug("closed alert popup about content")
        except selenium.common.exceptions.TimeoutException:
            pass

    def __do_retweet_pinned(self):
        retweet_count = 0
        # get a retweet div with an include pinned element
        pin_text_element = self.driver.find_element(By.XPATH,
                                                    "//div[@data-testid='socialContext' and contains(text(), 'Pinned')]")
        pin_text = pin_text_element.text  # Extract the text from the WebElement

        # get all tweets
        tweets = self.driver.find_elements(By.XPATH, "//*[@data-testid='tweet']")

        # check if the pinned text is in the tweet
        for tweet in tweets:
            if pin_text in tweet.text:
                # click on the tweet
                time.sleep(1)
                # scroll to the retweet button
                self.driver.vertical_scroller.scroll_to(500)
                # click on the retweet button
                try:
                    self.__do_retweet_pinned_media_element(tweet)
                    time.sleep(1)
                    retweet_count += 1
                    # increase the retweet count
                    return retweet_count
                except Exception as error:
                    self.__do_unretweet_pinned_media_element(tweet)
                    time.sleep(1)
                    self.__do_retweet_pinned_media_element(tweet)
                    time.sleep(1)
                    retweet_count += 1
                    # increase the retweet count
                    return retweet_count
    def __do_retweet_pinned_media_element(self, element):
        random_sleep(1, 3)
        retweet_button = element.find_element(By.XPATH, "//button[@data-testid='retweet']")
        self.driver.execute_script("arguments[0].click()", retweet_button)
        random_sleep(1, 3)
        retweet_button_confirm = element.find_element(By.XPATH, "//div[@data-testid='retweetConfirm']")
        self.driver.execute_script("arguments[0].click()", retweet_button_confirm)
        random_sleep(1, 3)

    def __do_unretweet_pinned_media_element(self, element):
        random_sleep(1, 3)
        unretweet_button = element.find_element(By.XPATH, "//button[@data-testid='unretweet']")
        self.driver.execute_script("arguments[0].click()", unretweet_button)
        random_sleep(1, 3)
        unretweet_button_confirm = element.find_element(By.XPATH, "//div[@data-testid='unretweetConfirm']")
        self.driver.execute_script("arguments[0].click()", unretweet_button_confirm)
        random_sleep(1, 3)

