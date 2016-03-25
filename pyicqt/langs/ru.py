# -*- coding: utf-8 -*-

# If you change or add any strings in this file please contact the translators listed below
# Everything must be in UTF-8
# Look for language codes here - http://www.w3.org/WAI/ER/IG/ert/iso639.htm


# Russian - evadim <evadim@evadim.ru>, Night Nord <NightNord@gmail.com> &
# _vt <vitalyster@gmail.com>
class ru:
    sessiongreeting = u"Это экспериментальный шлюз PyICQ-t. Если у вас возникли проблемы, обращайтесь в список рассылки - http://groups.google.com/group/py-transports/"
    authenticatetext = u"ВНИМАНИЕ: Регистрация состоит из двух шагов.  Сначала, введите ваши локальные имя пользователя и пароль.  Если вы ввели правильное имя пользователя и пароль, вы получите сообщение 'Регистрация завершена'.  Далее, снова выберите 'Зарегистрироваться' и вы получите предложение ввести имя пользователя и пароль от вашей учётной записи ICQ."
    registertext = u"Напишите ICQ-номер в поле <Имя пользователя> и пароль."
    notloggedin = u"Ошибка. Прежде чем отсылать сообщения нужно авторизоваться."
    notregistered = u"Извините, похоже что вы не зарегистрированы на этом шлюзе. Пожалуйста, зарегистрируйтесь и попробуйте снова. Если у вас есть проблемы с регистрацией - обратитесь к администратору XMPP-сервера."
    waitforlogin = u"Извините, это сообщение ещё не может быть доставлено. Пожалйста, попробуйте позже, когда шлюз закончит авторизацию."
    usernotonline = u"Этот пользователь сейчас не в сети."
    gatewaytranslator = u"Введите номер(UIN) пользователя ICQ."
    sessionnotactive = u"Ваша сессия ICQ сейчас неактивна."
    aimemailnotification = u"У вас %d новых сообщений в %s!\nПроверьте вашу почту в %s."
    searchnodataform = u"Используйте вложенную форму для поиска.  Если ваш XMPP-клиент не поддерживает Data Forms, использовать поиск будет невозможно."
    searchtitle = u"Поиск пользователей"
    searchinstructions = u"Укажите e-mail адресс, или любую другую информацию в соответствующих полях, для поиска подходящих пользователей в базе ICQ.  Если заполнено поле e-mail, все другие поля игнорируются."
    sessionslimit = u"Извините, вы не можете быть подключены к ICQ из-за того что слишком много сессий активно в данный момент. Попробуйте позже или выберите другой шлюз из списка http://www.jabberes.org/servers/servers_by_gateway_icq.html"
    command_CommandList = u"Команды PyICQt"
    command_Statistics = u"Статистика PyICQt"
    command_RosterRetrieval = u"Получить содержимое контакт-листа"
    command_ConnectUsers = u"Подключить всех зарегистрированных пользователей"
    command_Done = u"Команда выполнена"
    command_NoSession = u"Прежде чем выполнить эту команду нужно авторизоваться."
    command_ChangePassword = u"Изменить пароль ICQ"
    command_ChangePassword_Instructions = u"Введите текущий и новый пароли ICQ ниже."
    command_ChangePassword_NewPassword = u"Новый пароль"
    command_ChangePassword_NewPasswordAgain = u"Новый пароль (снова)"
    command_ChangePassword_OldPassword = u"Текущий пароль"
    command_ChangePassword_Mismatch = u"Новые пароли не совпадают."
    command_ChangePassword_Failed = u"Неудалось изменить пароль.  Скорее всего это произошло потому что текущий пароль неверен."
    command_EmailLookup = u"Поиск ICQ пользователей через email"
    command_EmailLookup_Instructions = u"Введите адрес электронной почты чтобы узнать screen name, которое с ним ассоциировано."
    command_EmailLookup_Email = u"E-Mail адрес"
    command_EmailLookup_Results = u"С введенным e-mail связаны следующие screen names:"
    command_EmailLookup_NoResults = u"Для введённого адреса соответствующего screen name не найдено"
    command_ChangeEmail = u"Изменить зарегистрированный e-mail адрес"
    command_ChangeEmail_Instructions = u"Ниже, введите новый e-mail адрес. \nСообщение о подтверждении будет выслано на ваш текущий адрес,\nесли вы не передумаете, адрес сменится в течении 72 часов."
    command_ChangeEmail_Email = u"E-Mail адрес"
    command_SetXStatus = u"Задать Х-статус"
    command_Settings = u"Настройки"
    command_FormatScreenName = u"Изменить формат screen name"
    command_FormatScreenName_Instructions = u"Ниже введите формат screen name.\nПомните о том что изменить можно только регистр и пробелы."
    command_FormatScreenName_FMTScreenName = u"Форматированное ScreenName"
    command_ConfirmAccount = u"Подтвердить ICQ аккаунт"
    command_ConfirmAccount_Complete = u"Запрос на подтверждение аккаунта отправлен.\nСкоро вы должны получить электронное письмо с инструкциями как продолжить процесс."
    command_ConfirmAccount_Failed = u"Невозможно запросить подтвеждение."
    command_ConfirmAccount_Unknown = u"Неожиданный результат подтверждения аккаунта"
    command_ICQURITranslate = u"Преобразовать ICQ URI"
    command_ICQURITranslate_Instructions = u"Введите ICQ URI и соответствуящая ему функция будет определена по URI."
    command_ICQURITranslate_URI = u"URI"
    command_ICQURITranslate_Failed = u"Невозможно определить функцию URI."
    command_UpdateMyVCard = u"Обновить VCard"
    command_Help = u"Помощь"

    help_documentation = u"Вы можете получить помощь по PyICQt в следующих местах:"
    help_mainwiki = u"Официальная wiki-страница"
    help_maillist = u"Официальный список рассылки"
    help_mainroom = u"Официальная комната поддержки"
    help_localwebsite = u"Сайт сервера"
    help_localroom = u"Комната поддержки сервера"
    help_localsupportjid = u"Контактный jid администратора"
    help_mainwiki_Desc = u"Страница описания PyICQt"
    help_maillist_Desc = u"Почтовый список рассылки py-transports"
    help_mainroom_Desc = u"Основная комната помощи"
    help_localwebsite_Desc = u"Сайт документации"
    help_localroom_Desc = u"Комната поддержки"
    help_localsupportjid_Desc = u"JID человека, который сможет ответить на ваши вопросы"

    alert_shutdown = u"Транспорт отключается. Пожалуйста, не волнуйтесь, он возобновит работу в ближайшее время."

    statistics_OnlineSessions = u"В сети"
    statistics_Uptime = u"Время работы"
    statistics_IncomingMessages = u"Входящих сообщений"
    statistics_OutgoingMessages = u"Исходящих сообщений"
    statistics_TotalSessions = u"Всего сессий"
    statistics_MaxConcurrentSessions = u"Сессий одновременно"
    statistics_MessageCount = u"Всего сообщений"
    statistics_FailedMessageCount = u"Ошибка отправки"
    statistics_AvatarCount = u"Передано аватар"
    statistics_FailedAvatarCount = u"Ошибка подсчёта аватар"
    statistics_OnlineSessions_Desc = u"Количество пользователей, которые сейчас подключены к сервису."
    statistics_Uptime_Desc = u"Время работы сервиса, в секундах."
    statistics_IncomingMessages_Desc = u"Количество сообщений, принятых из ICQ сети."
    statistics_OutgoingMessages_Desc = u"Количество сообщений, отправленных в ICQ сеть."
    statistics_TotalSessions_Desc = u"Количество подключений с момента запуска сервиса."
    statistics_MaxConcurrentSessions_Desc = u"Максимальное количество одновременных подключений к сервису."
    statistics_MessageCount_Desc = u"Количество сообщений, переданных и полученных из ICQ сети"
    statistics_FailedMessageCount_Desc = u"Количество вернувшихся сообщений, не дошедших до получателя"
    statistics_AvatarCount_Desc = u"Количество аватар, переданных и полученных из ICQ сети."
    statistics_FailedAvatarCount_Desc = u"Количество неудачных попыток передачи аватар."
    xstatus_set = u"X-статус установлен"
    xstatus_reset = u"Ваш X-статус сброшен"
    xstatus_support_disabled = u"Поддержка X-статусов отключена\n администратором сервера"
    xstatus_sending_disabled = u"Поддержка X-статусов отключена.\n Проверьте свои настройки"
    xstatus_set_xstatus_name = u"Задать имя X-статуса"
    xstatus_set_instructions = u"Выберите X-статус из списка"
    xstatus_no_xstatus = u"Нет X-статуса"
    xstatus_set_details = u"Задать X-статус и его описание"
    xstatus_name = u"Х-статус"
    xstatus_title = u"Название"
    xstatus_description = u"Описание"
    xstatus_set_instructions_Desc = u"Внимание: официальные клиенты поддерживают только 24 статуса (Сердитый - Печатаю), поддержка остальных статусов зависит от ICQ клиента"

    status_away = u"Отошел"
    status_dnd = u"Не беспокоить"
    status_xa = u"Отошел давно"
    status_chat = u"Готов поболтать"

    settings_category = u"Категория"
    settings_category_xstatus = u"Настройки X-статуса"
    settings_category_clist = u"Настройки списка контактов"
    settings_category_message = u"Настройки сообщений"
    settings_category_personal_events = u"Настройки оповещений"
    settings_category_autoanswer = u"Автоответчик"
    settings_instructions = u"Выберите категорию настроек"
    settings_changed = u"Настройки изменены успешно"
    settings_instructions_Desc = u"Внимание: Вам нужно переподключиться чтобы настройки отмеченные звёздочкой (*) вступили в силу"

    # contact list settings
    settings_clist_show_phantombuddies = u"* Показать временные ICQ контакты в ростере (найдено: %s)"
    settings_clist_deny_all_auth_requests = u"Блокировать запросы авторизации"
    settings_clist_show_phantombuddies_Desc = u"Полезно если Вы удалили нужный контакт и желаете его восстановить"
    settings_clist_deny_all_auth_requests_Desc = u"Транспорт будет отвечать отказом на все входящие запросы авторизации"

    # status settings
    away_messages_sending = u"Посылать сообщения об отстуствии"
    away_messages_receiving = u"Принимать сообщения об отстуствии"
    away_messages_sending_Desc = u"Посылать статус-сообщения пользователям ICQ в режиме 'Отсутствует' или 'Не доступен'"
    away_messages_receiving_Desc = u"Принимать статус-сообщения от пользователей ICQ в режиме 'Отсутствует' или 'Не доступен'"
    xstatus_sendmode = u"* Режим отправки X-статуса"
    xstatus_sendmode_none = u"Отключено"
    xstatus_sendmode_ICQ5 = u"ICQ 5.1 (наиболее популярно)"
    xstatus_sendmode_ICQ6 = u"ICQ 6 (меньше трафика)"
    xstatus_sendmode_ICQ5_6 = u"ICQ 5.1+6 (максимальная совместимость)"
    xstatus_sendmode_Desc = u"Посылать Х-статус пользователям ICQ в новом (ICQ6) или в старом (ICQ5.1) формате"
    xstatus_restore_after_disconnect = u"Восстанавливать X-статус после отключения"
    xstatus_restore_after_disconnect_Desc = u"Автоматически устанавливать Х-статус который использовался до отключения"
    xstatus_recvmode = u"Режим приёма X-статуса"
    xstatus_recvmode_none = u"Отключено"
    xstatus_recvmode_ICQ5 = u"ICQ 5.1 (наиболее популярно)"
    xstatus_recvmode_ICQ6 = u"ICQ 6 (меньше трафика)"
    xstatus_recvmode_ICQ5_6 = u"ICQ 5.1+6 (максимальная совместимость)"
    xstatus_recvmode_Desc = u"Принимать Х-статус от пользователей ICQ в новом (ICQ6) или в старом (ICQ5.1) формате"
    xstatus_option_smooth = u"Получать статус-иконки по протоколам  5.1 и 6"
    xstatus_option_smooth_Desc = u"Устраняет проблемы между старыми и новыми ICQ клиентами в области отображения Х-статусов"
    xstatus_display_icon_as_PEP = u"Отображать статус-иконку как событие"
    xstatus_display_icon_as_PEP_Desc = u"Отображать иконку Х-статуса, если Ваш XMPP клиент поддерживает PEP"
    xstatus_display_text_as_PEP = u" Отображать текст статуса как событие"
    xstatus_display_text_as_PEP_Desc = u"Отображать текст Х-статуса и иконку для него (если возможно)"
    xstatus_icon_for_transport = u" Отображать статус-иконку для транспорта"
    xstatus_icon_for_transport_Desc = u"Возможность видеть иконку собственного Х-статуса если XMPP-клиент это поддерживает"

    # message settings
    utf8_messages_sendmode = u"Посылать сообщения в utf-8"
    utf8_messages_sendmode_none = u"Отправка отключена"
    utf8_messages_sendmode_as_reply = u"В ответ на входящее сообщение в utf-8"
    utf8_messages_sendmode_always = u"Всегда"
    utf8_messages_sendmode_Desc = u"Сообщения в utf-8 позволяют решить проблему с кодировками"
    offline_messages_sendenc = u"Кодировка для исходящих оффлайн-сообщений"
    offline_messages_sendenc_unicode = u"Unicode"
    offline_messages_sendenc_local = u"Однобайтовая кодировка"
    offline_messages_sendenc_auto = u"Автоопределение"
    offline_messages_sendenc_Desc = u"Рекомендуется автоопределение"
    msgconfirm_sendmode = u"Режим отправки подтвеждений"
    msgconfirm_sendmode_none = u"Отправка отключена"
    msgconfirm_sendmode_for_utf8 = u"Только для сообщений в utf-8"
    msgconfirm_sendmode_always = u"Всегда"
    msgconfirm_sendmode_Desc = u"Посылать подтверждения (отчёт о доставке) для входящих сообщений"
    msgconfirm_recvmode = u"Приём подтвеждений"
    msgconfirm_recvmode_Desc = u"Принимать подтверждения для своих сообщений"

    # personal events settings
    user_mood_receiving = u"Показывать настроения"
    user_activity_receiving = u"Показывать занятия"
    user_tune_receiving = u"Показывать мелодии"
    user_mood_receiving_Desc = u"Иконка Х-статуса как настроение - поддерживается в Psi 0.11+, Gajim 0.12+, Jabbim 0.4+, Tkabber 0.11+, Coccinella 0.95+, Miranda IM 0.7+"
    user_activity_receiving_Desc = u"Иконка Х-статуса как занятие - поддерживается в Gajim 0.12+, Jabbim 0.4+, Tkabber 0.11+, Coccinella 0.96+, Miranda IM 0.8+"
    user_tune_receiving_Desc = u"Иконка Х-статуса как мелодия - поддерживается в Psi 0.11+, Gajim 0.12+, Jabbim 0.4+, Tkabber 0.11+, Miranda IM 0.7+"

    # auto-answer settings
    autoanswer_enable = u"Включть автоответчик"
    autoanswer_enable_Desc = u"Выбранный текст будет отправлен в качестве ответа на любое входящее сообщение"
    autoanswer_hide_dialog = u"Скрывать диалог автоответчика"
    autoanswer_hide_dialog_Desc = u"Скрывать входящие сообщения когда автоответчик отвечает на них"
    autoanswer_text = u"Текст"
    autoanswer_text_Desc = u"Текст автоответчика"
    autoanswer_text_content = u"Привет. Я отсутствую и не могу ответить прямо сейчас. Оставьте свое сообщение"
    autoanswer_prefix = u"[Автоответчик]"

    # additional "normal" statuses
    anstatus_out_to_lunch = u"Ем"
    anstatus_on_the_phone = u"Разговариваю по телефону"
    anstatus_at_home = u"Дома"
    anstatus_at_work = u"На работе"
    anstatus_evil = u"Злой"
    anstatus_depression = u"В депрессии"
    # x-statuses
    xstatus_angry = u"Сердитый"
    xstatus_taking_a_bath = u"В ванной"
    xstatus_tired = u"Уставший"
    xstatus_party = u"На вечеринке"
    xstatus_drinking_beer = u"Пью пиво"
    xstatus_thinking = u"Думаю"
    xstatus_eating = u"Ем"
    xstatus_watching_tv = u"Смотрю ТВ"
    xstatus_meeting = u"На встрече"
    xstatus_coffee = u"Кофе"
    xstatus_listening_to_music = u"Слушаю музыку"
    xstatus_business = u"Работаю"
    xstatus_shooting = u"Стреляю"
    xstatus_having_fun = u"Развлекаюсь"
    xstatus_on_the_phone = u"Разговариваю по телефону"
    xstatus_gaming = u"Играю"
    xstatus_studying = u"Учусь"
    xstatus_shopping = u"Шоппинг"
    xstatus_feeling_sick = u"Болею"
    xstatus_sleeping = u"Сплю"
    xstatus_surfing = u"Сёрфинг"
    xstatus_browsing = u"В интернете"
    xstatus_working = u"Работаю"
    xstatus_typing = u"Печатаю"
    xstatus_cn1 = u"Пикник"
    xstatus_cn2 = u"Счастливое"
    xstatus_cn3 = u"Болтаю"
    xstatus_cn4 = u"Я высоко!"
    xstatus_cn5 = u"В движении"
    xstatus_de1 = u"Быть или не быть?"
    xstatus_de2 = u"Смотрю кино"
    xstatus_de3 = u"Любовь"
    xstatus_ru1 = u"Ищу"
    xstatus_ru2 = u"Флирт"
    xstatus_ru3 = u"Пишу в дневник"
    # moods
    mood_afraid = 'Afraid'
    mood_amazed = 'Amazed'
    mood_angry = 'Angry'
    mood_annoyed = 'Annoyed'
    mood_anxious = 'Anxious'
    mood_aroused = 'Aroused'
    mood_ashamed = 'Ashamed'
    mood_bored = 'Bored'
    mood_brave = 'Brave'
    mood_calm = 'Calm'
    mood_cold = 'Cold'
    mood_confused = 'Confused'
    mood_contented = 'Contented'
    mood_cranky = 'Cranky'
    mood_curious = 'Curious'
    mood_depressed = 'Depressed'
    mood_disappointed = 'Disappointed'
    mood_disgusted = 'Disgusted'
    mood_distracted = 'Distracted'
    mood_embarrassed = 'Embarrassed'
    mood_excited = 'Excited'
    mood_flirtatious = 'Flirtatious'
    mood_frustrated = 'Frustrated'
    mood_grumpy = 'Grumpy'
    mood_guilty = 'Guilty'
    mood_happy = 'Happy'
    mood_hot = 'Hot'
    mood_humbled = 'Humbled'
    mood_humiliated = 'Humiliated'
    mood_hungry = 'Hungry'
    mood_hurt = 'Hurt'
    mood_impressed = 'Impressed'
    mood_in_awe = 'In awe'
    mood_in_love = 'In love'
    mood_indignant = 'Indignant'
    mood_interested = 'Interested'
    mood_intoxicated = 'Intoxicated'
    mood_invincible = 'Invincible'
    mood_jealous = 'Jealous'
    mood_lonely = 'Lonely'
    mood_mean = 'Mean'
    mood_moody = 'Moody'
    mood_nervous = 'Nervous'
    mood_neutral = 'Neutral'
    mood_offended = 'Offended'
    mood_playful = 'Playful'
    mood_proud = 'Proud'
    mood_relieved = 'Relieved'
    mood_remorseful = 'Remorseful'
    mood_restless = 'Restless'
    mood_sad = 'Sad'
    mood_sarcastic = 'Sarcastic'
    mood_serious = 'Serious'
    mood_shocked = 'Shocked'
    mood_shy = 'Shy'
    mood_sick = 'Sick'
    mood_sleepy = 'Sleepy'
    mood_stressed = 'Stressed'
    mood_surprised = 'Surprised'
    mood_thirsty = 'Thirsty'
    mood_worried = 'Worried'
    # activities
    act_doing_chores = 'Doing Chores'
    subact_buying_groceries = 'Buying Groceries'
    subact_cleaning = 'Cleaning'
    subact_cooking = 'Cooking'
    subact_doing_maintenance = 'Doing Maintenance'
    subact_doing_the_dishes = 'Doing the Dishes'
    subact_doing_the_laundry = 'Doing the Laundry'
    subact_gardening = 'Gardening'
    subact_running_an_errand = 'Running an Errand'
    subact_walking_the_dog = 'Walking the Dog'
    act_drinking = 'Drinking'
    subact_having_a_beer = 'Having a Beer'
    subact_having_coffee = 'Having Coffee'
    subact_having_tea = 'Having Tea'
    act_eating = 'Eating'
    subact_having_a_snack = 'Having a Snack'
    subact_having_breakfast = 'Having Breakfast'
    subact_having_dinner = 'Having Dinner'
    subact_having_lunch = 'Having Lunch'
    act_exercising = 'Exercising'
    subact_cycling = 'Cycling'
    subact_hiking = 'Hiking'
    subact_jogging = 'Jogging'
    subact_playing_sports = 'Playing Sports'
    subact_running = 'Running'
    subact_skiing = 'Skiing'
    subact_swimming = 'Swimming'
    subact_working_out = 'Working Out'
    act_grooming = 'Grooming'
    subact_at_the_spa = 'At the Spa'
    subact_brushing_teeth = 'Brushing Teeth'
    subact_getting_a_haircut = 'Getting a Haircut'
    subact_shaving = 'Shaving'
    subact_taking_a_bath = 'Taking a Bath'
    subact_taking_a_shower = 'Taking a Shower'
    act_having_appointment = 'Having an Appointment'
    act_inactive = 'Inactive'
    subact_day_off = 'Day Off'
    subact_hanging_out = 'Hanging Out'
    subact_on_vacation = 'On Vacation'
    subact_scheduled_holiday = 'Scheduled Holiday'
    subact_sleeping = 'Sleeping'
    act_relaxing = 'Relaxing'
    subact_gaming = 'Gaming'
    subact_going_out = 'Going Out'
    subact_partying = 'Partying'
    subact_reading = 'Reading'
    subact_rehearsing = 'Rehearsing'
    subact_shopping = 'Shopping'
    subact_socializing = 'Socializing'
    subact_sunbathing = 'Sunbathing'
    subact_watching_tv = 'Watching TV'
    watching_a_movie = 'Watching a Movie'
    act_talking = 'Talking'
    subact_in_real_life = 'In Real Life'
    subact_on_the_phone = 'On the Phone'
    subact_on_video_phone = 'On Video Phone'
    act_traveling = 'Traveling'
    subact_commuting = 'Commuting'
    subact_cycling = 'Cycling'
    subact_driving = 'Driving'
    subact_in_a_car = 'In a car'
    subact_on_a_bus = 'On a Bus'
    subact_on_a_plane = 'On a Plane'
    subact_on_a_train = 'On a Train'
    subact_on_a_trip = 'On a Trip'
    subact_walking = 'Walking'
    act_working = 'Working'
    subact_coding = 'Coding'
    subact_in_a_meeting = 'In a Meeting'
    subact_studying = 'Studying'
    subact_writing = 'Writing'

ru_RU = ru