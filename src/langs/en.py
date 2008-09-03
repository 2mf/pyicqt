# -*- coding: UTF-8 -*-

# If you change or add any strings in this file please contact the translators listed below
# Everything must be in UTF-8
# Look for language codes here - http://www.w3.org/WAI/ER/IG/ert/iso639.htm

class en: # English - James Bunton <mailto:james@delx.cjb.net>/Daniel Henninger <mailto:jadestorm@nc.rr.com>
	# Text that may get sent to the user. Useful for translations. Keep any %s symbols you see or you will have troubles later
	sessiongreeting = u"This is an experimental gateway, PyICQ-t. If you experience problems please contact Daniel Henninger <jadestorm@nc.rr.com>"
	authenticatetext = u"WARNING: Registration is a two-step process.  First, please enter your local username and your local password.  If you enter a valid username and password, you will get a 'Registration Successful' message.  Then, click Register again, and you will be prompted for your AIM username and password."
	registertext = u"Please type your ICQ user id number into the username field and your password."
	notloggedin = u"Error. You must log into the transport before sending messages."
	notregistered = u"Sorry. You do not appear to be registered with this transport. Please register and try again. If you are having trouble registering please contact your Jabber administrator."
	waitforlogin = u"Sorry, this message cannot be delivered yet. Please try again when the transport has finished logging in."
	usernotonline = u"The user you specified is not currently online."
	gatewaytranslator = u"Enter the user's ICQ user id number."
	sessionnotactive = u"Your session with ICQ is not active at this time."
	aimemailnotification = u"You have %d new message(s) at %s!\nCheck your mail at %s."
	searchnodataform = u"Use the enclosed form to search.  If your Jabber client does not support Data Forms, you will not be able to use this functionality."
	searchtitle = u"ICQ Directory Search"
	searchinstructions = u"Fill in either the e-mail address field or any number of the other fields to search the ICQ directory for matching users.  If the e-mail address is filled in, all other fields are ignored."
	command_CommandList = u"PyICQt Commands"
	command_Statistics = u"Statistics for PyICQt"
	command_RosterRetrieval = u"Retrieve Roster Contents"
	command_ConnectUsers = u"Connect all registered users"
	command_Done = u"Command completed"
	command_NoSession = u"You must be logged in to use this command."
	command_ChangePassword = u"Change ICQ password"
	command_ChangePassword_Instructions = u"Enter your current and new ICQ passwords below."
	command_ChangePassword_NewPassword = u"New password"
	command_ChangePassword_NewPasswordAgain = u"New password (again)"
	command_ChangePassword_OldPassword = u"Current password"
	command_ChangePassword_Mismatch = u"New passwords entered do not match."
	command_ChangePassword_Failed = u"Password change failed.  Most likely this is due to the wrong current password being entered."
	command_EmailLookup = u"Look up ICQ users via email"
	command_EmailLookup_Instructions = u"Enter an email address below to locate screen names associated with it."
	command_EmailLookup_Email = u"E-Mail address"
	command_EmailLookup_Results = u"These screen names matched the address provided:"
	command_ChangeEmail = u"Change registered e-mail address"
	command_ChangeEmail_Instructions = u"Enter your new e-mail address below.\nA confirmation message will be sent to your current address and,\nunless you cancel, your new address will take effect in 72 hours."
	command_ChangeEmail_Email = u"E-Mail address"
	command_SetXStatus = u"Set x-status" #TODO: make translation for other languages
	command_Settings = u"Settings" #TODO: make translation for other languages
	command_FormatScreenName = u"Change format of screen name"
	command_FormatScreenName_Instructions = u"Enter format of screen name below.\nPlease be aware that only capitalization and spacing may be changed."
	command_FormatScreenName_FMTScreenName = u"Formatted ScreenName"
	command_ConfirmAccount = u"Confirm ICQ account"
	command_ConfirmAccount_Complete = u"Account confirmation request completed.\nYou should receive email soon with instructions on how to proceed."
	command_ConfirmAccount_Failed = u"Unable to request confirmation at this time."
	command_ICQURITranslate = u"Translate an ICQ URI"
	command_ICQURITranslate_Instructions = u"Enter an ICQ URI and appropriate action will be taken based off the function of the URI."
	command_ICQURITranslate_URI = u"URI"
	command_ICQURITranslate_Failed = u"Unable to determine function of URI."
	command_UpdateMyVCard = u"Update my VCard"
	statistics_OnlineSessions = u"Online Users"
	statistics_Uptime = u"Uptime"
	statistics_IncomingMessages = u"Incoming Messages"
	statistics_OutgoingMessages = u"Outgoing Messages"
	statistics_TotalSessions = u"Total Sessions"
	statistics_MaxConcurrentSessions = u"Max Concurrent Sessions"
	statistics_MessageCount = u"Message Count"
	statistics_FailedMessageCount = u"Failed Message Count"
	statistics_AvatarCount = u"Avatar Count"
	statistics_FailedAvatarCount = u"Failed Avatar Count"
	statistics_OnlineSessions_Desc = u"The number of users currently connected to the service."
	statistics_Uptime_Desc = u"How long the service has been running, in seconds."
	statistics_IncomingMessages_Desc = u"How many messages have been transferred from the ICQ network."
	statistics_OutgoingMessages_Desc = u"How many messages have been transferred to the ICQ network."
	statistics_TotalSessions_Desc = u"The number of connections since the service started."
	statistics_MaxConcurrentSessions_Desc = u"The maximum number of users connected at any one time."
	statistics_MessageCount_Desc = u"How many messages have been transferred to and from the ICQ network."
	statistics_FailedMessageCount_Desc = u"The number of messages that didn't make it to the ICQ recipient and were bounced."
	statistics_AvatarCount_Desc = u"How many avatars have been transferred to and from the ICQ network."
	statistics_FailedAvatarCount_Desc = u"The number of avatar transfers that have failed."
	xstatus_set = u"Your x-status has been set"
	xstatus_support_disabled = u"X-status support disabled\n by your administrator"
	xstatus_sending_disabled = u"X-status sending support disabled.\n Check your settings for details"
	xstatus_set_xstatus_name = u"Set x-status name"
	xstatus_set_instructions = u"Select x-status from list below\nNote: official clients supports only 24 statuses\n(Angry - Typing), support for other could be\ndepends from ICQ client"
	xstatus_no_xstatus = u"No x-status"
	xstatus_set_details = u"Set x-status title and description"
	xstatus_name = u"Name"
	xstatus_title = u"Title"
	xstatus_description = u"Description"
	settings_category = u"Category"
	settings_category_xstatus = u"Status settings"
	settings_category_clist = u"Contact list settings"
	settings_category_message = u"Message settings"
	settings_instructions = u"Options marked with asterisk required\n re-login for applying changes"
	settings_xstatus_restore_after_disconnect = u"Restore latest x-status after disconnect"
	# contact list settings
	settings_clist_show_phantombuddies = u"* Show temporary ICQ contacts in roster (%s found)"
	# status settings
	away_messages_receiving = u"Away messages receiving"
	xstatus_sendmode = u"X-statuses sending mode"
	xstatus_sendmode_none = u"None"
	xstatus_sendmode_ICQ5 = u"ICQ 5.1 (most popular)"
	xstatus_sendmode_ICQ6 = u"ICQ 6 (less traffic)"
	xstatus_sendmode_ICQ5_6 = u"ICQ 5.1+6 (max compatibility)"
	xstatus_recvmode = u"X-statuses receiving mode"
	xstatus_recvmode_none = u"None"
	xstatus_recvmode_ICQ5 = u"ICQ 5.1 (most popular)"
	xstatus_recvmode_ICQ6 = u"ICQ 6 (less traffic)"
	xstatus_recvmode_ICQ5_6 = u"ICQ 5.1+6 (max compatibility)"
	xstatus_option_smooth = u"Allow status icons between 5.1 and 6"
	xstatus_display_icon_as_PEP = u"Display status icon as mood/activity"
	xstatus_display_text_as_PEP = u"Try display status text as mood/activity"
	# message settings
	utf8_messages_sendmode = u"utf-8 messages sending mode"
	utf8_messages_sendmode_none = u"Sending disabled"
	utf8_messages_sendmode_as_reply = u"As reply on incoming utf-8 message"
	utf8_messages_sendmode_always = u"Always when it's possible"
	send_confirm_for_ut8_msg = u"Send confirmations for incoming utf-8 messages"
	# additional "normal" statuses
	anstatus_out_to_lunch = u"Out to lunch"
	anstatus_on_the_phone = u"On the phone"
	anstatus_at_home = u"At home"
	anstatus_at_work = u"At work"
	anstatus_evil = u"Evil"
	anstatus_depression = u"Depression"
	# x-statuses
	xstatus_angry = u"Angry"
	xstatus_taking_a_bath = u"Taking a bath"
	xstatus_tired = u"Tired"
	xstatus_party = u"Party"
	xstatus_drinking_beer = u"Drinking beer"
	xstatus_thinking = u"Thinking"
	xstatus_eating = u"Eating"
	xstatus_watching_tv = u"Watching TV"
	xstatus_meeting = u"Meeting"
	xstatus_coffee = u"Coffee"
	xstatus_listening_to_music = u"Listening to music"
	xstatus_business = u"Business"
	xstatus_shooting = u"Shooting"
	xstatus_having_fun = u"Having fun"
	xstatus_on_the_phone = u"On the phone"
	xstatus_gaming = u"Gaming"
	xstatus_studying = u"Studying"
	xstatus_shopping = u"Shopping"
	xstatus_feeling_sick = u"Feeling sick"
	xstatus_sleeping = u"Sleeping"
	xstatus_surfing = u"Surfing"
	xstatus_browsing = u"Browsing"
	xstatus_working = u"Working"
	xstatus_typing = u"Typing"
	xstatus_cn1 = u"Picnic"
	xstatus_cn2 = u"Happy"
	xstatus_cn3 = u"Chit chatting"
	xstatus_cn4 = u"I\"m high"
	xstatus_cn5 = u"I\"m mooving"
	xstatus_de1 = u"To be or not to be"
	xstatus_de2 = u"Watching a movie"
	xstatus_de3 = u"Love"
	xstatus_ru1 = u"Searching"
	xstatus_ru2 = u"Flirt"
	xstatus_ru3 = u"Blogging"
	# these lines for adding to user's status
	xstatus_append_status = u"Status"
	xstatus_append_xstatus = u"X-status"
	xstatus_append_xmessage = u"X-message"
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
	
en_US = en # en-US is the same as en, so are the others
en_AU = en
en_GB = en
