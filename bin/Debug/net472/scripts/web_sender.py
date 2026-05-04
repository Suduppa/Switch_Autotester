import asyncio
import traceback
from playwright.async_api import async_playwright

data_manager = None

async def _log_result(sheet_name, command, status, output, target_value="N/A"):
    if data_manager:
        data_manager.sync_add_result(
            test_source=sheet_name,
            command=command,
            status=status,
            output=output[:1000],
            target_value=target_value
        )
    print(f"[WEB] {command} -> {status}")

async def run_web_test(ip, user, password, test_name, sheet_name="WEB"):
    url = f"http://{ip}"
    
    async with async_playwright() as p:
        try:
            #headless=True - невидимый режим
            browser = await p.chromium.launch(headless=False)
            
            context = await browser.new_context(
                ignore_https_errors=True,
                http_credentials={'username': user, 'password': password}
            )
            page = await context.new_page()


            #Доступность
            if test_name == "web__availability":
                response = await page.goto(url, wait_until="networkidle", timeout=15000)
                if response and response.ok:
                    await _log_result(sheet_name, "Открыть web-интерфейс", "Успех", f"Страница загружена. Статус: {response.status}", "HTTP 200")
                else:
                    await _log_result(sheet_name, "Открыть web-интерфейс", "Ошибка", f"Сбой загрузки. Статус: {response.status if response else 'Нет ответа'}", "HTTP 200")

            # навигация и сохранение
            elif test_name == "web__navigation":
                #await asyncio.sleep(47)
                await page.goto(url, wait_until="networkidle")
                await page.fill("input[name='luci_username']", user)
                await page.fill("input[name='luci_password']", password)
                await page.click("input[type='submit'][value='Войти']")
                await page.wait_for_load_state("networkidle")

                menu_links = await page.locator("#mainmenu a").all()
                urls_to_visit = []

                for link in menu_links:
                    href = await link.get_attribute("href")
                    menu_text = await link.inner_text()
                    menu_text = menu_text.strip()

                    if href and href != "#":
                        if "logout" not in href and "reboot" not in href and "flash" not in href:
                            urls_to_visit.append((menu_text, href))

                urls_to_visit = list(dict.fromkeys(urls_to_visit))
                
                await _log_result(sheet_name, "Сбор ссылок меню", "Успех", f"Найдено безопасных страниц для обхода: {len(urls_to_visit)}", "Список собран")

                for menu_name, link_url in urls_to_visit:
                    try:
                        full_url = link_url
                        if link_url.startswith("/"):
                            full_url = f"http://{ip}{link_url}"
                        elif not link_url.startswith("http"):
                            full_url = f"http://{ip}/{link_url}"

                        await page.goto(full_url, wait_until="networkidle")
                        await asyncio.sleep(1)
                        
                        error_locators = page.locator("div.alert-message:visible, div.error:visible, .cbi-value-error:visible")
                        error_count = await error_locators.count()

                        if error_count > 0:
                            error_text = await error_locators.first.inner_text()
                            clean_error_text = error_text.replace('\n', ' ').strip()
                            await _log_result(sheet_name, f"Вкладка: {menu_name}", "Ошибка", f"Найден блок ошибки: {clean_error_text[:100]}", "Без ошибок")
                        else:
                            await _log_result(sheet_name, f"Вкладка: {menu_name}", "Успех", "Страница отрисована корректно", "Без ошибок")
                            
                    except Exception as nav_err:
                        await _log_result(sheet_name, f"Вкладка: {menu_name}", "Ошибка", f"Сбой загрузки: {str(nav_err)}", "Без ошибок")
                        
                await _log_result(sheet_name, "Тест обхода меню (UI Errors)", "Выполнено", "Все доступные вкладки проверены", "Завершение")


            #перевод
            elif test_name == "web__translation":
                await page.goto(url, wait_until="networkidle")
                await page.fill("input[name='luci_username']", user)
                await page.fill("input[name='luci_password']", password)
                await page.click("input[type='submit'][value='Войти']")
                await page.wait_for_load_state("networkidle")

                await page.click("text=ru")
                await page.wait_for_load_state("networkidle")
                await page.click("text=Язык")
                await page.wait_for_load_state("networkidle")
                # Выбираем Английский
                lang_select_id = '[id="widget.cbid.luci.tfortis._lang"]'
                await page.select_option(lang_select_id, "English")
                await asyncio.sleep(1)
                await page.click("text=применить")
                await _log_result(sheet_name, "Конфигурация применена", "Успех", "Язык переключен", "en")
                await page.wait_for_load_state("networkidle")
                await asyncio.sleep(10)
                # Выбираем Русский
                await page.select_option(lang_select_id, "Русский (Russian)")
                await asyncio.sleep(1)
                await page.click("text=save & apply")
                await asyncio.sleep(10)
                await _log_result(sheet_name, "Конфигурация применена", "Успех", "Язык переключен", "ru")

#пользователи WEB
            elif test_name == "web__user__management":
                
                async def do_login(l_user, l_pass):
                    await page.goto(f"http://{ip}/cgi-bin/luci/", wait_until="networkidle")
                    if await page.locator("input[name='luci_username']").count() > 0:
                        await page.locator("input[name='luci_username']").fill(l_user)
                        await page.locator("input[name='luci_password']").fill(l_pass)
                        await page.locator("input[type='submit'][value='Войти']").click()
                        await page.wait_for_load_state("networkidle")

                async def do_logout():
                    await page.goto(f"http://{ip}/cgi-bin/luci/admin/logout", wait_until="networkidle")

                try:
                    await do_login(user, password)
                    await page.goto(f"http://{ip}/cgi-bin/luci/admin/system/acl", wait_until="networkidle")

                    body_text = await page.locator("body").inner_text()
                    if "root" not in body_text:
                        await _log_result(sheet_name, "Проверка невидимости root", "Успех", "Пользователь root не отображается", "Отсутствие root")
                    else:
                        await _log_result(sheet_name, "Проверка невидимости root", "Ошибка", "Пользователь root виден в интерфейсе", "Отсутствие root")

                    #Создание test_full (Полный доступ)
                    await page.click("text=Добавить") 
                    await page.wait_for_selector(".modal", state="visible")
                  
                    await page.locator('div[data-name="username"] input').fill("test_full")
                    await page.locator('div[data-name="password"] input').fill("12345")
                    await page.locator('div[data-name="password_confirm"] input').fill("12345")
                    await page.locator('div[data-name="_level"] select').select_option(index=1)
                    await page.locator('.modal').locator('text=СОХРАНИТЬ').click()
                    #await page.wait_for_selector(".modal", state="hidden")
                    #await page.click('text=ПРИМЕНИТЬ')
                    await page.wait_for_load_state("networkidle")
                    await _log_result(sheet_name, "Создание test_full", "Успех", "Создан пользователь с полным доступом", "test_full")

                    #Создание test_user (Только чтение)
                    await page.click("text=Добавить")
                    await page.wait_for_selector(".modal", state="visible")
                    
                    await page.locator('div[data-name="username"] input').fill("test_user")
                    await page.locator('div[data-name="password"] input').fill("222")
                    await page.locator('div[data-name="password_confirm"] input').fill("222")
                    await page.locator('div[data-name="_level"] select').select_option(index=2)
                    await page.locator('.modal').locator('text=СОХРАНИТЬ').click()
                    #await page.wait_for_selector(".modal", state="hidden")
                    await page.click('text=ПРИМЕНИТЬ')
                    await page.wait_for_load_state("networkidle")
                    await _log_result(sheet_name, "Создание test_user", "Успех", "Создан пользователь read-only", "test_user")
                    await asyncio.sleep(10)

                    #Проверка прав test_full
                    await do_logout()
                    await do_login("test_full", "12345")
                    await page.goto(f"http://{ip}/cgi-bin/luci/admin/system/system", wait_until="networkidle")
                    await asyncio.sleep(2) # время на отрисовку
                    
                    save_btn_full = page.locator(".cbi-button-save, .cbi-button-apply").first
                    if await save_btn_full.count() > 0:
                        if not await save_btn_full.is_disabled():
                            await _log_result(sheet_name, "Проверка прав test_full", "Успех", "Кнопка 'Сохранить' АКТИВНА (Полный доступ)", "Кнопка активна")
                        else:
                            await _log_result(sheet_name, "Проверка прав test_full", "Ошибка", "Кнопка 'Сохранить' найдена, но НЕАКТИВНА", "Кнопка активна")
                    else:
                        await _log_result(sheet_name, "Проверка прав test_full", "Ошибка", "У test_full нет кнопок сохранения (не отрисовались)", "Кнопка найдена")

                    #Проверка прав test_user
                    await do_logout()
                    await do_login("test_user", "222")
                    await page.goto(f"http://{ip}/cgi-bin/luci/admin/system/system", wait_until="networkidle")
                    await asyncio.sleep(2) # время на отрисовку
                    
                    save_btn_user = page.locator(".cbi-button-save, .cbi-button-apply").first
                    if await save_btn_user.count() > 0:
                        if await save_btn_user.is_disabled():
                            await _log_result(sheet_name, "Проверка прав test_user", "Успех", "Кнопка 'Сохранить' ЗАБЛОКИРОВАНА (Только чтение)", "Кнопка заблокирована")
                        else:
                            await _log_result(sheet_name, "Проверка прав test_user", "Ошибка", "У пользователя Read-Only кнопка 'Сохранить' АКТИВНА", "Кнопка заблокирована")
                    else:
                        await _log_result(sheet_name, "Проверка прав test_user", "Успех", "Кнопка 'Сохранить' полностью скрыта (Только чтение)", "Кнопка скрыта")

                    #удаление тестовых учеток   
                    await do_logout()
                    await do_login(user, password)
                    await page.goto(f"http://{ip}/cgi-bin/luci/admin/system/acl", wait_until="networkidle")
                    await asyncio.sleep(2) 
                    
                    users_to_delete = ["test_full", "test_user"]
                    deleted_count = 0
                    
                    for u_name in users_to_delete:
                        row_locator = page.locator(".cbi-section-table-row, tr").filter(has_text=u_name).first
                        
                        if await row_locator.count() > 0:
                            del_btn = row_locator.locator(".cbi-button-remove").first
                            if await del_btn.count() > 0:
                                await del_btn.click()
                                await asyncio.sleep(1)
                                deleted_count += 1
                    await page.click ("text=Применить")  #Можно написать грамотнее, 2 раза кликает по кнопке применить
                    await asyncio.sleep(10) 
                    if deleted_count > 0:
                        await page.locator('.cbi-button-save, .cbi-button-apply').first.click()
                        await page.wait_for_load_state("networkidle")
                        await _log_result(sheet_name, "Уборка: Удаление пользователей", "Успех", f"Удалено пользователей: {deleted_count}", "Очистка")
                    else:
                        await _log_result(sheet_name, "Уборка: Удаление пользователей", "Ошибка", "Скрипт не нашел созданных пользователей в таблице", "Очистка")
                except Exception as e:
                    await _log_result(sheet_name, "Работа с пользователями WEB", "Ошибка", f"Сбой скрипта: {str(e)}", "Выполнено")

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"[WEB Error] {error_trace}")
            await _log_result(sheet_name, f"Web тест ({test_name})", "Критическая ошибка", str(e), "Выполнение")
        finally:
            await browser.close()