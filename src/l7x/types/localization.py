#####################################################################################################

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum
from logging import Logger
from re import MULTILINE, UNICODE, Match, compile as _re_compile
from typing import Final

from l7x.types.language import LKey
from l7x.types.mapping import FrozenDict

#####################################################################################################
# AUTOGENERATE_BEGIN
# !!! dont change manually, use
#   ./src/_l10n.py sync

# pylint: disable=line-too-long, too-many-lines
#####################################################################################################

_DIALOG_PLACEHOLDER_MAP: Final = FrozenDict({
    LKey.AR: 'انقر على الميكروفون وابدأ بالتحدث',
    LKey.AZ: 'Mikrofona basın və danışmağa başlayın',
    LKey.DE: 'Klicken Sie auf das Mikrofon und beginnen Sie zu sprechen',
    LKey.EN: 'Click on the microphone and start talking',
    LKey.ES: 'Haz clic en el micrófono y comienza a hablar.',
    LKey.FR: 'Cliquez sur le microphone et commencez à parler',
    LKey.HI: 'माइक्रोफ़ोन पर क्लिक करें और बात करना शुरू करें',
    LKey.HU: 'Kattintson a mikrofonra, és kezdjen el beszélni',
    LKey.KO: '마이크를 클릭하고 말하기를 시작하세요',
    LKey.NE: 'माइक्रोफोनमा क्लिक गर्नुहोस् र कुरा सुरु गर्नुहोस्',
    LKey.PA: "ਮਾਈਕ੍ਰੋਫੋਨ 'ਤੇ ਕਲਿੱਕ ਕਰੋ ਅਤੇ ਗੱਲ ਸ਼ੁਰੂ ਕਰੋ",
    LKey.RU: 'Нажмите на микрофон и начните говорить.',
    LKey.TG: 'Микрофонро клик кунед ва сӯҳбатро оғоз кунед',
    LKey.TL: 'Mag-click sa mikropono at magsimulang magsalita',
    LKey.UR: 'مائکروفون پر کلک کریں اور بات کرنا شروع کریں۔',
    LKey.UZ: 'Mikrofonni bosing va suhbatni boshlang',
    LKey.ZH: '点击麦克风并开始讲话',
})

#####################################################################################################

_END_DIALOG_MAP: Final = FrozenDict({
    LKey.AR: 'انهاء الحوار',
    LKey.AZ: 'Dialoqu bitirin',
    LKey.DE: 'Beenden des Dialogs',
    LKey.EN: 'End the dialog',
    LKey.ES: 'Finalizar el diálogo',
    LKey.FR: 'Mettre fin au dialogue',
    LKey.HI: 'संवाद समाप्त करें',
    LKey.HU: 'Zárja be a párbeszédpanelt',
    LKey.KO: '대화 종료',
    LKey.NE: 'संवाद अन्त्य गर्नुहोस्',
    LKey.PA: 'ਡਾਇਲਾਗ ਸਮਾਪਤ ਕਰੋ',
    LKey.RU: 'Завершить диалог',
    LKey.TG: 'Муколамаро хотима диҳед',
    LKey.TL: 'Tapusin ang dialog',
    LKey.UR: 'ڈائیلاگ ختم کریں۔',
    LKey.UZ: 'Muloqot oynasini tugatish',
    LKey.ZH: '结束对话',
})

#####################################################################################################

_START_DIALOG_MAP: Final = FrozenDict({
    LKey.AR: 'ابدأ الحوار',
    LKey.AZ: 'Dialoqa başlayın',
    LKey.DE: 'Starten Sie den Dialog',
    LKey.EN: 'Start the dialog',
    LKey.ES: 'Iniciar el diálogo',
    LKey.FR: 'Démarrer le dialogue',
    LKey.HI: 'संवाद प्रारंभ करें',
    LKey.HU: 'Indítsa el a párbeszédpanelt',
    LKey.KO: '대화 시작',
    LKey.NE: 'संवाद सुरु गर्नुहोस्',
    LKey.PA: 'ਡਾਇਲਾਗ ਸ਼ੁਰੂ ਕਰੋ',
    LKey.RU: 'Начать диалог',
    LKey.TG: 'Муколамаро оғоз кунед',
    LKey.TL: 'Simulan ang dialog',
    LKey.UR: 'ڈائیلاگ شروع کریں۔',
    LKey.UZ: 'Muloqot oynasini boshlang',
    LKey.ZH: '开始对话',
})

#####################################################################################################

_CLOSE_POPUP_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'هل ترغب في إنهاء الحوار؟',
    LKey.AZ: 'Dialoqu bitirmək istərdinizmi?',
    LKey.DE: 'Möchten Sie den Dialog beenden?',
    LKey.EN: 'Would you like to end the dialog?',
    LKey.ES: '¿Quieres finalizar el diálogo?',
    LKey.FR: 'Souhaitez-vous mettre fin au dialogue?',
    LKey.HI: 'क्या आप संवाद समाप्त करना चाहेंगे?',
    LKey.HU: 'Be szeretné fejezni a párbeszédet?',
    LKey.KO: '대화를 종료하시겠습니까?',
    LKey.NE: 'के तपाइँ संवाद अन्त्य गर्न चाहनुहुन्छ?',
    LKey.PA: 'ਕੀ ਤੁਸੀਂ ਡਾਇਲਾਗ ਨੂੰ ਖਤਮ ਕਰਨਾ ਚਾਹੋਗੇ?',
    LKey.RU: 'Хотите завершить диалог?',
    LKey.TG: 'Мехоҳед муколамаро хотима диҳед?',
    LKey.TL: 'Gusto mo bang tapusin ang dialog?',
    LKey.UR: 'کیا آپ ڈائیلاگ ختم کرنا چاہیں گے؟',
    LKey.UZ: 'Muloqotni tugatishni xohlaysizmi?',
    LKey.ZH: '您想结束对话吗？',
})

#####################################################################################################

_CLOSE_POPUP_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'سيكون من المستحيل العودة ومواصلة الحوار بعد الانتهاء.',
    LKey.AZ: 'Tamamlandıqdan sonra geri qayıtmaq və dialoqa davam etmək mümkün olmayacaq.',
    LKey.DE: 'Es ist nicht möglich, nach Abschluss zurückzukehren und den Dialog fortzusetzen.',
    LKey.EN: 'It will be impossible to return and continue the dialog after completion.',
    LKey.ES: 'Será imposible regresar y continuar el diálogo una vez finalizado.',
    LKey.FR: 'Il sera impossible de revenir et de poursuivre le dialogue une fois terminé.',
    LKey.HI: 'पूरा होने के बाद वापस लौटना और संवाद जारी रखना असंभव होगा।',
    LKey.HU: 'Lehetetlen lesz visszatérni és folytatni a párbeszédet a befejezés után.',
    LKey.KO: '완료된 후에는 돌아가서 대화를 계속하는 것이 불가능합니다.',
    LKey.NE: 'यो फर्कन असम्भव हुनेछ र पूरा भएपछि संवाद जारी राख्न।',
    LKey.PA: 'ਸੰਪੂਰਨ ਹੋਣ ਤੋਂ ਬਾਅਦ ਡਾਇਲਾਗ ਨੂੰ ਵਾਪਸ ਕਰਨਾ ਅਤੇ ਜਾਰੀ ਰੱਖਣਾ ਅਸੰਭਵ ਹੋਵੇਗਾ।',
    LKey.RU: 'После завершения вернуться и продолжить диалог будет невозможно.',
    LKey.TG: 'Пас аз ба итмом расидани муколама баргаштан ва идома додан ғайриимкон хоҳад буд.',
    LKey.TL: 'Imposibleng ibalik at ipagpatuloy ang dialog pagkatapos makumpleto.',
    LKey.UR: 'مکمل ہونے کے بعد واپسی اور ڈائیلاگ کو جاری رکھنا ناممکن ہو جائے گا۔',
    LKey.UZ: "Tugallangandan keyin qaytish va dialogni davom ettirish imkonsiz bo'ladi.",
    LKey.ZH: '完成后将无法返回并继续对话。',
})

#####################################################################################################

_CLOSE_POPUP_END_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'نهاية',
    LKey.AZ: 'Son',
    LKey.DE: 'Ende',
    LKey.EN: 'End',
    LKey.ES: 'Fin',
    LKey.FR: 'Fin',
    LKey.HI: 'अंत',
    LKey.HU: 'Vége',
    LKey.KO: '끝',
    LKey.NE: 'अन्त्य',
    LKey.PA: 'ਅੰਤ',
    LKey.RU: 'Конец',
    LKey.TG: 'Поён',
    LKey.TL: 'Tapusin',
    LKey.UR: 'ختم',
    LKey.UZ: 'Oxiri',
    LKey.ZH: '结尾',
})

#####################################################################################################

_CLOSE_POPUP_CONTINUE_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'متابعة الحوار',
    LKey.AZ: 'Dialoqu davam etdirin',
    LKey.DE: 'Den Dialog fortsetzen',
    LKey.EN: 'Сontinue the dialog',
    LKey.ES: 'Continuar el diálogo',
    LKey.FR: 'Poursuivre le dialogue',
    LKey.HI: 'संवाद जारी रखें',
    LKey.HU: 'Folytassa a párbeszédpanelt',
    LKey.KO: '대화를 계속하세요',
    LKey.NE: 'संवाद जारी राख्नुहोस्',
    LKey.PA: 'ਡਾਇਲਾਗ ਜਾਰੀ ਰੱਖੋ',
    LKey.RU: 'Продолжить диалог',
    LKey.TG: 'Муколамаро идома диҳед',
    LKey.TL: 'Ipagpatuloy ang dialog',
    LKey.UR: 'ڈائیلاگ جاری رکھیں',
    LKey.UZ: 'Dialogni davom ettiring',
    LKey.ZH: '继续对话',
})

#####################################################################################################

_NEXT_SURVAY_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'التالي',
    LKey.AZ: 'Sonrakı',
    LKey.DE: 'Nächste',
    LKey.EN: 'Next',
    LKey.ES: 'Próximo',
    LKey.FR: 'Suivant',
    LKey.HI: 'अगला',
    LKey.HU: 'Következő',
    LKey.KO: '다음',
    LKey.NE: 'अर्को',
    LKey.PA: 'ਅਗਲਾ',
    LKey.RU: 'Следующий',
    LKey.TG: 'Баъдӣ',
    LKey.TL: 'Susunod',
    LKey.UR: 'اگلا',
    LKey.UZ: 'Keyingisi',
    LKey.ZH: '下一个',
})

#####################################################################################################

_SKIP_SURVAY_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'أو تخطي الاستطلاع',
    LKey.AZ: 'və ya sorğunu keçin',
    LKey.DE: 'oder Überspringen Sie die Umfrage',
    LKey.EN: 'or Skip the survey',
    LKey.ES: 'o Saltar la encuesta',
    LKey.FR: "ou ignorer l'enquête",
    LKey.HI: 'या सर्वेक्षण छोड़ें',
    LKey.HU: 'vagy Kihagyja a felmérést',
    LKey.KO: '또는 설문조사를 건너뛰세요',
    LKey.NE: 'वा सर्वेक्षण छोड्नुहोस्',
    LKey.PA: 'ਜਾਂ ਸਰਵੇਖਣ ਛੱਡੋ',
    LKey.RU: 'или пропустить опрос',
    LKey.TG: 'ё Пурсишро гузаред',
    LKey.TL: 'o Laktawan ang survey',
    LKey.UR: 'یا سروے کو چھوڑ دیں۔',
    LKey.UZ: "yoki So'rovni o'tkazib yuboring",
    LKey.ZH: '或跳过调查',
})

#####################################################################################################

_QUESTION_MAP: Final = FrozenDict({
    LKey.AR: 'سؤال',
    LKey.AZ: 'Sual',
    LKey.DE: 'Frage',
    LKey.EN: 'Question',
    LKey.ES: 'Pregunta',
    LKey.FR: 'Question',
    LKey.HI: 'सवाल',
    LKey.HU: 'Kérdés',
    LKey.KO: '질문',
    LKey.NE: 'प्रश्न',
    LKey.PA: 'ਸਵਾਲ',
    LKey.RU: 'Вопрос',
    LKey.TG: 'Савол',
    LKey.TL: 'Tanong',
    LKey.UR: 'سوال',
    LKey.UZ: 'Savol',
    LKey.ZH: '问题',
})

#####################################################################################################

_OF_MAP: Final = FrozenDict({
    LKey.AR: 'ل',
    LKey.AZ: 'of',
    LKey.DE: 'von',
    LKey.EN: 'of',
    LKey.ES: 'de',
    LKey.FR: 'de',
    LKey.HI: 'का',
    LKey.HU: 'a',
    LKey.KO: '~의',
    LKey.NE: 'को',
    LKey.PA: 'ਦੇ',
    LKey.RU: 'из',
    LKey.TG: 'аз',
    LKey.TL: 'ng',
    LKey.UR: 'کی',
    LKey.UZ: 'ning',
    LKey.ZH: '的',
})

#####################################################################################################

_SURVAY_ONE_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'يرجى تقييم مدى سهولة استخدامك للمترجم على مقياس من 1 إلى 5.',
    LKey.AZ: 'Zəhmət olmasa, tərcüməçidən istifadə etməyin sizin üçün nə qədər asan olduğunu 1-dən 5-ə qədər miqyasda qiymətləndirin.',
    LKey.DE: 'Bitte bewerten Sie auf einer Skala von 1 bis 5, wie einfach die Verwendung des Übersetzers für Sie war.',
    LKey.EN: 'Please rate on a scale from 1 to 5 how easy it was for you to use the translator.',
    LKey.ES: 'Califique en una escala del 1 al 5 lo fácil que le resultó utilizar el traductor.',
    LKey.FR: 'Veuillez évaluer sur une échelle de 1 à 5 la facilité avec laquelle vous avez pu utiliser le traducteur.',
    LKey.HI: 'कृपया 1 से 5 के पैमाने पर रेटिंग दें कि आपके लिए अनुवादक का उपयोग करना कितना आसान था।',
    LKey.HU: 'Kérjük, értékelje egy 1-től 5-ig terjedő skálán, hogy milyen egyszerű volt a fordító használata.',
    LKey.KO: '번역기를 사용하는 것이 얼마나 쉬웠는지 1~5점 척도로 평가해 주세요.',
    LKey.NE: 'कृपया 1 देखि 5 सम्मको स्केलमा मूल्याङ्कन गर्नुहोस् कि तपाईलाई अनुवादक प्रयोग गर्न कति सजिलो थियो।',
    LKey.PA: "ਕਿਰਪਾ ਕਰਕੇ 1 ਤੋਂ 5 ਦੇ ਪੈਮਾਨੇ 'ਤੇ ਰੇਟ ਕਰੋ ਕਿ ਤੁਹਾਡੇ ਲਈ ਅਨੁਵਾਦਕ ਦੀ ਵਰਤੋਂ ਕਰਨਾ ਕਿੰਨਾ ਆਸਾਨ ਸੀ।",
    LKey.RU: 'Оцените по шкале от 1 до 5, насколько легко вам было пользоваться переводчиком.',
    LKey.TG: 'Лутфан аз рӯи ҷадвали аз 1 то 5 баҳо диҳед, ки чӣ тавр истифода бурдани тарҷумон барои шумо осон буд.',
    LKey.TL: 'Paki-rate sa isang sukat mula 1 hanggang 5 kung gaano kadali para sa iyo na gamitin ang tagasalin.',
    LKey.UR: 'براہ کرم 1 سے 5 کے پیمانے پر درجہ بندی کریں کہ آپ کے لیے مترجم کو استعمال کرنا کتنا آسان تھا۔',
    LKey.UZ: "Iltimos, tarjimondan foydalanish qanchalik oson bo'lganini 1 dan 5 gacha bo'lgan shkala bo'yicha baholang.",
    LKey.ZH: '请按 1 到 5 的等级评价您使用翻译器的难易程度。',
})

#####################################################################################################

_SURVAY_ONE_RATE_ONE_MAP: Final = FrozenDict({
    LKey.AR: 'صعب جدا',
    LKey.AZ: 'Çox çətin',
    LKey.DE: 'Sehr schwierig',
    LKey.EN: 'Very difficult',
    LKey.ES: 'Muy difícil',
    LKey.FR: 'Très difficile',
    LKey.HI: 'बहुत कठिन',
    LKey.HU: 'Nagyon nehéz',
    LKey.KO: '매우 어렵다',
    LKey.NE: 'धेरै गाह्रो',
    LKey.PA: 'ਬਹੁਤ ਔਖਾ',
    LKey.RU: 'Очень сложно',
    LKey.TG: 'Хеле душвор',
    LKey.TL: 'Napakahirap',
    LKey.UR: 'بہت مشکل',
    LKey.UZ: 'Juda qiyin',
    LKey.ZH: '非常困难',
})

#####################################################################################################

_SURVAY_ONE_RATE_TWO_MAP: Final = FrozenDict({
    LKey.AR: 'صعب',
    LKey.AZ: 'Çətin',
    LKey.DE: 'Schwierig',
    LKey.EN: 'Difficult',
    LKey.ES: 'Difícil',
    LKey.FR: 'Difficile',
    LKey.HI: 'कठिन',
    LKey.HU: 'Nehéz',
    LKey.KO: '어려운',
    LKey.NE: 'गाह्रो',
    LKey.PA: 'ਔਖਾ',
    LKey.RU: 'Трудный',
    LKey.TG: 'Мушкил',
    LKey.TL: 'Mahirap',
    LKey.UR: 'مشکل',
    LKey.UZ: 'Qiyin',
    LKey.ZH: '难的',
})

#####################################################################################################

_SURVAY_ONE_RATE_THREE_MAP: Final = FrozenDict({
    LKey.AR: 'حيادي',
    LKey.AZ: 'Neytral',
    LKey.DE: 'Neutral',
    LKey.EN: 'Neutral',
    LKey.ES: 'Neutral',
    LKey.FR: 'Neutre',
    LKey.HI: 'तटस्थ',
    LKey.HU: 'Semleges',
    LKey.KO: '중립적',
    LKey.NE: 'तटस्थ',
    LKey.PA: 'ਨਿਰਪੱਖ',
    LKey.RU: 'Нейтральный',
    LKey.TG: 'Бетараф',
    LKey.TL: 'Neutral',
    LKey.UR: 'غیر جانبدار',
    LKey.UZ: 'Neytral',
    LKey.ZH: '中性的',
})

#####################################################################################################

_SURVAY_ONE_RATE_FOUR_MAP: Final = FrozenDict({
    LKey.AR: 'سهل',
    LKey.AZ: 'Asan',
    LKey.DE: 'Einfach',
    LKey.EN: 'Easy',
    LKey.ES: 'Fácil',
    LKey.FR: 'Facile',
    LKey.HI: 'आसान',
    LKey.HU: 'Könnyen',
    LKey.KO: '쉬운',
    LKey.NE: 'सजिलो',
    LKey.PA: 'ਆਸਾਨ',
    LKey.RU: 'Легкий',
    LKey.TG: 'Осон',
    LKey.TL: 'Madali',
    LKey.UR: 'آسان',
    LKey.UZ: 'Oson',
    LKey.ZH: '简单的',
})

#####################################################################################################

_SURVAY_ONE_RATE_FIVE_MAP: Final = FrozenDict({
    LKey.AR: 'سهل جدا',
    LKey.AZ: 'Çox asan',
    LKey.DE: 'Sehr leicht',
    LKey.EN: 'Very easy',
    LKey.ES: 'Muy fácil',
    LKey.FR: 'Très facile',
    LKey.HI: 'बहुत आसान',
    LKey.HU: 'Nagyon könnyű',
    LKey.KO: '매우 쉽습니다',
    LKey.NE: 'धेरै सजिलो',
    LKey.PA: 'ਬਹੁਤ ਆਸਾਨ',
    LKey.RU: 'Очень легко',
    LKey.TG: 'Хеле осон',
    LKey.TL: 'Napakadali',
    LKey.UR: 'بہت آسان',
    LKey.UZ: 'Juda oson',
    LKey.ZH: '非常简单',
})

#####################################################################################################

_SURVAY_TWO_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'يرجى تقييم من 1 إلى 5 لمدى احتمالية أن توصي بخدمتنا إلى صديق أو زميل.',
    LKey.AZ: 'Xidmətimizi dostunuza və ya həmkarınıza tövsiyə etmək ehtimalınızı 1-dən 5-ə qədər qiymətləndirin.',
    LKey.DE: 'Bitte bewerten Sie auf einer Skala von 1 bis 5, wie wahrscheinlich es ist, dass Sie unseren Service einem Freund oder Kollegen weiterempfehlen würden.',
    LKey.EN: 'Please rate from 1 to 5 how likely you are to recommend our service to a friend or a colleague.',
    LKey.ES: 'Califique del 1 al 5 la probabilidad de que recomiende nuestro servicio a un amigo o colega.',
    LKey.FR: 'Veuillez évaluer de 1 à 5 la probabilité que vous recommandiez notre service à un ami ou à un collègue.',
    LKey.HI: 'कृपया 1 से 5 तक रेटिंग दें कि आप किसी मित्र या सहकर्मी को हमारी सेवा की कितनी संभावना से अनुशंसा करेंगे।',
    LKey.HU: 'Kérjük, értékelje 1-től 5-ig, mekkora valószínűséggel ajánlja szolgáltatásunkat barátjának vagy kollégájának.',
    LKey.KO: '친구나 동료에게 당사의 서비스를 추천할 가능성을 1~5점으로 평가해 주세요.',
    LKey.NE: 'कृपया 1 देखि 5 सम्मको मूल्याङ्कन गर्नुहोस् कि तपाईले हाम्रो सेवालाई साथी वा सहकर्मीलाई सिफारिस गर्ने सम्भावना कति छ।',
    LKey.PA: 'ਕਿਰਪਾ ਕਰਕੇ 1 ਤੋਂ 5 ਤੱਕ ਰੇਟ ਕਰੋ ਕਿ ਤੁਸੀਂ ਕਿਸੇ ਦੋਸਤ ਜਾਂ ਸਹਿਕਰਮੀ ਨੂੰ ਸਾਡੀ ਸੇਵਾ ਦੀ ਸਿਫਾਰਸ਼ ਕਰਨ ਦੀ ਕਿੰਨੀ ਸੰਭਾਵਨਾ ਰੱਖਦੇ ਹੋ।',
    LKey.RU: 'Оцените по шкале от 1 до 5, насколько вероятно, что вы порекомендуете наши услуги другу или коллеге.',
    LKey.TG: 'Лутфан аз 1 то 5 баҳо диҳед, ки то чӣ андоза шумо хидмати моро ба дӯст ё ҳамкоратон тавсия медиҳед.',
    LKey.TL: 'Paki-rate mula 1 hanggang 5 kung gaano mo malamang na irekomenda ang aming serbisyo sa isang kaibigan o kasamahan.',
    LKey.UR: 'براہ کرم 1 سے 5 تک درجہ بندی کریں کہ آپ کسی دوست یا ساتھی کو ہماری خدمت کی سفارش کرنے کا کتنا امکان رکھتے ہیں۔',
    LKey.UZ: "Iltimos, do'stingizga yoki hamkasbingizga bizning xizmatimizni tavsiya qilish ehtimolini 1 dan 5 gacha baholang.",
    LKey.ZH: '请从 1 到 5 评分，说明您向朋友或同事推荐我们服务的可能性。',
})

#####################################################################################################

_SURVAY_TWO_RATE_ONE_MAP: Final = FrozenDict({
    LKey.AR: 'من غير المحتمل جدًا',
    LKey.AZ: 'Çox az ehtimal',
    LKey.DE: 'Sehr unwahrscheinlich',
    LKey.EN: 'Very Unlikely',
    LKey.ES: 'Muy improbable',
    LKey.FR: 'Très peu probable',
    LKey.HI: 'बहुत संभावना नहीं',
    LKey.HU: 'Nagyon valószínűtlen',
    LKey.KO: '매우 가능성 없음',
    LKey.NE: 'धेरै असम्भव',
    LKey.PA: 'ਬਹੁਤ ਅਸੰਭਵ',
    LKey.RU: 'Очень маловероятно',
    LKey.TG: 'Ба эҳтимоли зиёд',
    LKey.TL: 'Very Unlikely',
    LKey.UR: 'بہت غیر امکان',
    LKey.UZ: 'Juda kam',
    LKey.ZH: '非常不可能',
})

#####################################################################################################

_SURVAY_TWO_RATE_TWO_MAP: Final = FrozenDict({
    LKey.AR: 'من غير المحتمل',
    LKey.AZ: 'Ehtimal yoxdur',
    LKey.DE: 'Unwahrscheinlich',
    LKey.EN: 'Unlikely',
    LKey.ES: 'Improbable',
    LKey.FR: 'Peu probable',
    LKey.HI: 'संभावना नहीं',
    LKey.HU: 'Valószínűtlen',
    LKey.KO: '할 것 같지 않은',
    LKey.NE: 'असम्भव',
    LKey.PA: 'ਅਸੰਭਵ',
    LKey.RU: 'Маловероятно',
    LKey.TG: 'Аз эҳтимол дур аст',
    LKey.TL: 'Hindi malamang',
    LKey.UR: 'امکان نہیں ہے۔',
    LKey.UZ: 'Darhaqiqat',
    LKey.ZH: '不太可能',
})

#####################################################################################################

_SURVAY_TWO_RATE_THREE_MAP: Final = FrozenDict({
    LKey.AR: 'حيادي',
    LKey.AZ: 'Neytral',
    LKey.DE: 'Neutral',
    LKey.EN: 'Neutral',
    LKey.ES: 'Neutral',
    LKey.FR: 'Neutre',
    LKey.HI: 'तटस्थ',
    LKey.HU: 'Semleges',
    LKey.KO: '중립적',
    LKey.NE: 'तटस्थ',
    LKey.PA: 'ਨਿਰਪੱਖ',
    LKey.RU: 'Нейтральный',
    LKey.TG: 'Бетараф',
    LKey.TL: 'Neutral',
    LKey.UR: 'غیر جانبدار',
    LKey.UZ: 'Neytral',
    LKey.ZH: '中性的',
})

#####################################################################################################

_SURVAY_TWO_RATE_FOUR_MAP: Final = FrozenDict({
    LKey.AR: 'محتمل',
    LKey.AZ: 'Ehtimal ki',
    LKey.DE: 'Wahrscheinlich',
    LKey.EN: 'Likely',
    LKey.ES: 'Probable',
    LKey.FR: 'Probable',
    LKey.HI: 'संभावित',
    LKey.HU: 'Valószínűleg',
    LKey.KO: '할 것 같은',
    LKey.NE: 'सम्भावित',
    LKey.PA: 'ਸੰਭਾਵਤ',
    LKey.RU: 'Вероятный',
    LKey.TG: 'Эҳтимол',
    LKey.TL: 'Malamang',
    LKey.UR: 'امکان',
    LKey.UZ: 'Ehtimol',
    LKey.ZH: '有可能',
})

#####################################################################################################

_SURVAY_TWO_RATE_FIVE_MAP: Final = FrozenDict({
    LKey.AR: 'من المرجح جدًا',
    LKey.AZ: 'Çox Ehtimal',
    LKey.DE: 'Sehr wahrscheinlich',
    LKey.EN: 'Very Likely',
    LKey.ES: 'Muy probable',
    LKey.FR: 'Très probable',
    LKey.HI: 'बहुत संभावना है',
    LKey.HU: 'Nagyon valószínű',
    LKey.KO: '매우 가능성이 높다',
    LKey.NE: 'धेरै सम्भावित',
    LKey.PA: 'ਬਹੁਤ ਸੰਭਾਵਨਾ ਹੈ',
    LKey.RU: 'Очень вероятно',
    LKey.TG: 'Эҳтимоли зиёд',
    LKey.TL: 'Malamang',
    LKey.UR: 'بہت امکان ہے۔',
    LKey.UZ: 'Juda ehtimol',
    LKey.ZH: '非常有可能',
})

#####################################################################################################

_SURVAY_THREE_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'يرجى تقييم جودة الترجمة على مقياس من 1 إلى 5.',
    LKey.AZ: 'Zəhmət olmasa tərcümənin keyfiyyətini 1-dən 5-ə qədər olan şkala ilə qiymətləndirin.',
    LKey.DE: 'Bitte bewerten Sie die Qualität der Übersetzung auf einer Skala von 1 bis 5.',
    LKey.EN: 'Please rate the quality of translation on a scale from 1 to 5.',
    LKey.ES: 'Califique la calidad de la traducción en una escala del 1 al 5.',
    LKey.FR: 'Veuillez évaluer la qualité de la traduction sur une échelle de 1 à 5.',
    LKey.HI: 'कृपया अनुवाद की गुणवत्ता को 1 से 5 के पैमाने पर रेट करें।',
    LKey.HU: 'Kérjük, értékelje a fordítás minőségét egy 1-től 5-ig terjedő skálán.',
    LKey.KO: '번역의 질을 1~5점으로 평가해 주시기 바랍니다.',
    LKey.NE: 'कृपया 1 देखि 5 सम्मको स्केलमा अनुवादको गुणस्तर मूल्याङ्कन गर्नुहोस्।',
    LKey.PA: "ਕਿਰਪਾ ਕਰਕੇ 1 ਤੋਂ 5 ਦੇ ਪੈਮਾਨੇ 'ਤੇ ਅਨੁਵਾਦ ਦੀ ਗੁਣਵੱਤਾ ਨੂੰ ਦਰਜਾ ਦਿਓ।",
    LKey.RU: 'Оцените качество перевода по шкале от 1 до 5.',
    LKey.TG: 'Лутфан ба сифати тарҷума аз 1 то 5 баҳо диҳед.',
    LKey.TL: 'Paki-rate ang kalidad ng pagsasalin sa isang sukat mula 1 hanggang 5.',
    LKey.UR: 'براہ کرم ترجمے کے معیار کو 1 سے 5 کے پیمانے پر درجہ دیں۔',
    LKey.UZ: 'Tarjima sifatini 1 dan 5 gacha boʻlgan shkala boʻyicha baholang.',
    LKey.ZH: '请按 1 到 5 的等级对翻译质量进行评分。',
})

#####################################################################################################

_SURVAY_THREE_RATE_ONE_MAP: Final = FrozenDict({
    LKey.AR: 'رهيب',
    LKey.AZ: 'Dəhşətli',
    LKey.DE: 'Schrecklich',
    LKey.EN: 'Terrible',
    LKey.ES: 'Horrible',
    LKey.FR: 'Terrible',
    LKey.HI: 'भयानक',
    LKey.HU: 'Szörnyű',
    LKey.KO: '끔찍한',
    LKey.NE: 'भयानक',
    LKey.PA: 'ਭਿਆਨਕ',
    LKey.RU: 'Ужасный',
    LKey.TG: 'Даҳшатнок',
    LKey.TL: 'Grabe',
    LKey.UR: 'خوفناک',
    LKey.UZ: 'Dahshatli',
    LKey.ZH: '糟糕的',
})

#####################################################################################################

_SURVAY_THREE_RATE_TWO_MAP: Final = FrozenDict({
    LKey.AR: 'سيء',
    LKey.AZ: 'Pis',
    LKey.DE: 'Schlecht',
    LKey.EN: 'Bad',
    LKey.ES: 'Malo',
    LKey.FR: 'Mauvais',
    LKey.HI: 'खराब',
    LKey.HU: 'Rossz',
    LKey.KO: '나쁜',
    LKey.NE: 'खराब',
    LKey.PA: 'ਬੁਰਾ',
    LKey.RU: 'Плохой',
    LKey.TG: 'Бад',
    LKey.TL: 'Masama',
    LKey.UR: 'برا',
    LKey.UZ: 'Yomon',
    LKey.ZH: '坏的',
})

#####################################################################################################

_SURVAY_THREE_RATE_THREE_MAP: Final = FrozenDict({
    LKey.AR: 'طبيعي',
    LKey.AZ: 'Normal',
    LKey.DE: 'Normal',
    LKey.EN: 'Normal',
    LKey.ES: 'Normal',
    LKey.FR: 'Normale',
    LKey.HI: 'सामान्य',
    LKey.HU: 'Normál',
    LKey.KO: '정상',
    LKey.NE: 'सामान्य',
    LKey.PA: 'ਸਧਾਰਣ',
    LKey.RU: 'Нормальный',
    LKey.TG: 'Муқаррарӣ',
    LKey.TL: 'Normal',
    LKey.UR: 'نارمل',
    LKey.UZ: 'Oddiy',
    LKey.ZH: '普通的',
})

#####################################################################################################

_SURVAY_THREE_RATE_FOUR_MAP: Final = FrozenDict({
    LKey.AR: 'جيد',
    LKey.AZ: 'yaxşı',
    LKey.DE: 'Gut',
    LKey.EN: 'Good',
    LKey.ES: 'Bien',
    LKey.FR: 'Bien',
    LKey.HI: 'अच्छा',
    LKey.HU: 'Jó',
    LKey.KO: '좋은',
    LKey.NE: 'राम्रो',
    LKey.PA: 'ਚੰਗਾ',
    LKey.RU: 'Хороший',
    LKey.TG: 'Хуб',
    LKey.TL: 'Mabuti',
    LKey.UR: 'اچھا',
    LKey.UZ: 'Yaxshi',
    LKey.ZH: '好的',
})

#####################################################################################################

_SURVAY_THREE_RATE_FIVE_MAP: Final = FrozenDict({
    LKey.AR: 'ممتاز',
    LKey.AZ: 'Mükəmməl',
    LKey.DE: 'Perfekt',
    LKey.EN: 'Perfect',
    LKey.ES: 'Perfecto',
    LKey.FR: 'Parfait',
    LKey.HI: 'उत्तम',
    LKey.HU: 'Tökéletes',
    LKey.KO: '완벽한',
    LKey.NE: 'उत्तम',
    LKey.PA: 'ਸੰਪੂਰਣ',
    LKey.RU: 'Идеальный',
    LKey.TG: 'Комил',
    LKey.TL: 'Perpekto',
    LKey.UR: 'کامل',
    LKey.UZ: 'Mukammal',
    LKey.ZH: '完美的',
})

#####################################################################################################

_REVIEW_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'يرجى مشاركتنا بأفكارك حول الخدمة بشكل عام.',
    LKey.AZ: 'Zəhmət olmasa xidmət haqqında ümumi fikirlərinizi bölüşün.',
    LKey.DE: 'Bitte teilen Sie uns Ihre allgemeine Meinung zum Service mit.',
    LKey.EN: 'Please share your thoughts about the service in general.',
    LKey.ES: 'Por favor comparta sus opiniones sobre el servicio en general.',
    LKey.FR: 'Merci de partager vos réflexions sur le service en général.',
    LKey.HI: 'कृपया सेवा के बारे में अपने विचार साझा करें।',
    LKey.HU: 'Kérjük, ossza meg véleményét a szolgáltatásról általában.',
    LKey.KO: '서비스 전반에 대한 생각을 공유해 주세요.',
    LKey.NE: 'कृपया सेवाको बारेमा सामान्य रूपमा आफ्नो विचार साझा गर्नुहोस्।',
    LKey.PA: 'ਕਿਰਪਾ ਕਰਕੇ ਸੇਵਾ ਬਾਰੇ ਆਪਣੇ ਵਿਚਾਰ ਸਾਂਝੇ ਕਰੋ।',
    LKey.RU: 'Поделитесь, пожалуйста, своими мыслями об услуге в целом.',
    LKey.TG: 'Лутфан фикрҳои худро дар бораи хидмат дар маҷмӯъ мубодила кунед.',
    LKey.TL: 'Mangyaring ibahagi ang iyong mga saloobin tungkol sa serbisyo sa pangkalahatan.',
    LKey.UR: 'براہ کرم عام طور پر سروس کے بارے میں اپنے خیالات کا اشتراک کریں۔',
    LKey.UZ: 'Iltimos, xizmat haqida umumiy fikringizni bildiring.',
    LKey.ZH: '请分享您对该服务的总体看法。',
})

#####################################################################################################

_REVIEW_PLACEHOLDER_MAP: Final = FrozenDict({
    LKey.AR: 'اضغط لبدء الكتابة أو تسجيل الصوت',
    LKey.AZ: 'Səs yazmağa və ya yazmağa başlamaq üçün toxunun',
    LKey.DE: 'Tippen Sie hier, um mit dem Schreiben oder Aufzeichnen einer Stimme zu beginnen',
    LKey.EN: 'Tap to start writing or record voice',
    LKey.ES: 'Toque para comenzar a escribir o grabar voz.',
    LKey.FR: 'Appuyez pour commencer à écrire ou à enregistrer la voix',
    LKey.HI: 'लिखना शुरू करने या आवाज़ रिकॉर्ड करने के लिए टैप करें',
    LKey.HU: 'Érintse meg az írás vagy hangfelvétel megkezdéséhez',
    LKey.KO: '쓰기를 시작하거나 음성을 녹음하려면 탭하세요',
    LKey.NE: 'लेखन सुरु गर्न वा आवाज रेकर्ड गर्न ट्याप गर्नुहोस्',
    LKey.PA: 'ਲਿਖਣਾ ਸ਼ੁਰੂ ਕਰਨ ਜਾਂ ਆਵਾਜ਼ ਰਿਕਾਰਡ ਕਰਨ ਲਈ ਟੈਪ ਕਰੋ',
    LKey.RU: 'Нажмите, чтобы начать писать или записывать голос',
    LKey.TG: 'Барои оғоз кардани навиштан ё сабти овоз клик кунед',
    LKey.TL: 'I-tap para magsimulang magsulat o mag-record ng boses',
    LKey.UR: 'لکھنا شروع کرنے یا آواز ریکارڈ کرنے کے لیے تھپتھپائیں۔',
    LKey.UZ: 'Yozishni yoki ovoz yozishni boshlash uchun bosing',
    LKey.ZH: '点击开始书写或录音',
})

#####################################################################################################

_REVIEW_BOTTOM_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'يمكنك تخطي هذا السؤال وإنهاء الاستطلاع على الفور',
    LKey.AZ: 'Bu sualı atlaya və anketi dərhal bitirə bilərsiniz',
    LKey.DE: 'Sie können diese Frage überspringen und die Umfrage sofort beenden',
    LKey.EN: 'You can skip this question and finish the survey straight away',
    LKey.ES: 'Puede omitir esta pregunta y finalizar la encuesta inmediatamente.',
    LKey.FR: "Vous pouvez ignorer cette question et terminer l'enquête directement",
    LKey.HI: 'आप इस प्रश्न को छोड़ कर सीधे सर्वेक्षण समाप्त कर सकते हैं',
    LKey.HU: 'Kihagyhatja ezt a kérdést, és azonnal befejezheti a felmérést',
    LKey.KO: '이 질문을 건너뛰고 바로 설문조사를 마칠 수 있습니다.',
    LKey.NE: 'तपाइँ यो प्रश्न छोड्न सक्नुहुन्छ र तुरुन्तै सर्वेक्षण समाप्त गर्न सक्नुहुन्छ',
    LKey.PA: 'ਤੁਸੀਂ ਇਸ ਸਵਾਲ ਨੂੰ ਛੱਡ ਸਕਦੇ ਹੋ ਅਤੇ ਸਰਵੇਖਣ ਨੂੰ ਤੁਰੰਤ ਪੂਰਾ ਕਰ ਸਕਦੇ ਹੋ',
    LKey.RU: 'Вы можете пропустить этот вопрос и закончить опрос прямо сейчас.',
    LKey.TG: 'Шумо метавонед ин саволро гузаред ва дарҳол пурсишро анҷом диҳед',
    LKey.TL: 'Maaari mong laktawan ang tanong na ito at tapusin kaagad ang survey',
    LKey.UR: 'آپ اس سوال کو چھوڑ سکتے ہیں اور فوراً سروے مکمل کر سکتے ہیں۔',
    LKey.UZ: "Siz bu savolni o'tkazib yuborishingiz va so'rovni darhol tugatishingiz mumkin",
    LKey.ZH: '您可以跳过此问题并直接完成调查',
})

#####################################################################################################

_FINISH_SURVAY_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'إنهاء المسح',
    LKey.AZ: 'Anketi tamamlayın',
    LKey.DE: 'Beenden Sie die Umfrage',
    LKey.EN: 'Finish the survey',
    LKey.ES: 'Terminar la encuesta',
    LKey.FR: "Terminer l'enquête",
    LKey.HI: 'सर्वेक्षण समाप्त करें',
    LKey.HU: 'Fejezd be a felmérést',
    LKey.KO: '설문조사를 마치세요',
    LKey.NE: 'सर्वेक्षण समाप्त गर्नुहोस्',
    LKey.PA: 'ਸਰਵੇਖਣ ਨੂੰ ਪੂਰਾ ਕਰੋ',
    LKey.RU: 'Завершить опрос',
    LKey.TG: 'Пурсишро анҷом диҳед',
    LKey.TL: 'Tapusin ang survey',
    LKey.UR: 'سروے مکمل کریں۔',
    LKey.UZ: "So'rovni yakunlang",
    LKey.ZH: '完成调查',
})

#####################################################################################################

_BACK_TO_MENU_BTN_MAP: Final = FrozenDict({
    LKey.AR: 'العودة إلى القائمة',
    LKey.AZ: 'Menyuya qayıt',
    LKey.DE: 'Zurück zum Menü',
    LKey.EN: 'Back to menu',
    LKey.ES: 'Volver al menú',
    LKey.FR: 'Retour au menu',
    LKey.HI: 'मैन्यू में वापस',
    LKey.HU: 'Vissza a menühöz',
    LKey.KO: '메뉴로 돌아가기',
    LKey.NE: 'मेनुमा फर्कनुहोस्',
    LKey.PA: "ਮੀਨੂ 'ਤੇ ਵਾਪਸ ਜਾਓ",
    LKey.RU: 'Вернуться в меню',
    LKey.TG: 'Бозгашт ба меню',
    LKey.TL: 'Bumalik sa menu',
    LKey.UR: 'مینو پر واپس جائیں۔',
    LKey.UZ: 'Menyuga qaytish',
    LKey.ZH: '返回菜单',
})

#####################################################################################################

_FINAL_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'شكرا على إجاباتك!',
    LKey.AZ: 'Cavablarınız üçün təşəkkür edirik!',
    LKey.DE: 'Vielen Dank für Ihre Antworten!',
    LKey.EN: 'Thank you for your answers!',
    LKey.ES: '¡Gracias por tus respuestas!',
    LKey.FR: 'Merci pour vos réponses!',
    LKey.HI: 'आपके जवाब के लिए धन्यवाद!',
    LKey.HU: 'Köszönöm a válaszokat!',
    LKey.KO: '여러분의 답변에 감사드립니다!',
    LKey.NE: 'तपाईंको जवाफहरूको लागि धन्यवाद!',
    LKey.PA: 'ਤੁਹਾਡੇ ਜਵਾਬਾਂ ਲਈ ਧੰਨਵਾਦ!',
    LKey.RU: 'Спасибо за ваши ответы!',
    LKey.TG: 'Ташаккур барои ҷавобҳоятон!',
    LKey.TL: 'Salamat sa iyong mga sagot!',
    LKey.UR: 'آپ کے جوابات کے لیے آپ کا شکریہ!',
    LKey.UZ: 'Javoblaringiz uchun rahmat!',
    LKey.ZH: '感谢您的回答！',
})

#####################################################################################################

_LANG_SELECT_TITLE_MAP: Final = FrozenDict({
    LKey.AR: 'اختر اللغة المفضلة لديك',
    LKey.AZ: 'Tercih etdiyiniz dili seçin',
    LKey.DE: 'Wählen Sie Ihre bevorzugte Sprache',
    LKey.EN: 'Select your preferred language',
    LKey.ES: 'Seleccione su idioma preferido',
    LKey.FR: 'Sélectionnez votre langue préférée',
    LKey.HI: 'अपनी पसंदीदा भाषा चुनें',
    LKey.HU: 'Válassza ki a kívánt nyelvet',
    LKey.KO: '원하는 언어를 선택하세요',
    LKey.NE: 'आफ्नो मनपर्ने भाषा चयन गर्नुहोस्',
    LKey.PA: 'ਆਪਣੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਚੁਣੋ',
    LKey.RU: 'Выберите предпочитаемый язык',
    LKey.TG: 'Забони дӯстдоштаи худро интихоб кунед',
    LKey.TL: 'Piliin ang iyong gustong wika',
    LKey.UR: 'اپنی پسند کی زبان منتخب کریں۔',
    LKey.UZ: "O'zingiz yoqtirgan tilni tanlang",
    LKey.ZH: '选择您的首选语言',
})

#####################################################################################################

_EDITING_MAP: Final = FrozenDict({
    LKey.AR: 'تحرير',
    LKey.AZ: 'Redaktə',
    LKey.DE: 'Bearbeitung',
    LKey.EN: 'Editing',
    LKey.ES: 'Edición',
    LKey.FR: 'Édition',
    LKey.HI: 'संपादन',
    LKey.HU: 'Szerkesztés',
    LKey.KO: '편집 중',
    LKey.NE: 'सम्पादन गर्दै',
    LKey.PA: 'ਸੰਪਾਦਨ',
    LKey.RU: 'Редактирование',
    LKey.TG: 'Таҳрир',
    LKey.TL: 'Pag-edit',
    LKey.UR: 'ایڈیٹنگ',
    LKey.UZ: 'Tahrirlash',
    LKey.ZH: '編輯',
})

#####################################################################################################

_T_ARABIC_MAP: Final = FrozenDict({
    LKey.AR: 'عربي',
    LKey.AZ: 'ərəb',
    LKey.DE: 'Arabisch',
    LKey.EN: 'Arabic',
    LKey.ES: 'árabe',
    LKey.FR: 'arabe',
    LKey.HI: 'अरबी',
    LKey.HU: 'arab',
    LKey.KO: '아라비아 말',
    LKey.NE: 'अरबी',
    LKey.PA: 'ਅਰਬੀ',
    LKey.RU: 'арабский',
    LKey.TG: 'арабӣ',
    LKey.TL: 'Arabic',
    LKey.UR: 'عربی',
    LKey.UZ: 'arabcha',
    LKey.ZH: '阿拉伯',
})

#####################################################################################################

_T_AZERBAIJANI_MAP: Final = FrozenDict({
    LKey.AR: 'أذربيجاني',
    LKey.AZ: 'Azərbaycan',
    LKey.DE: 'Aserbaidschanisch',
    LKey.EN: 'Azerbaijani',
    LKey.ES: 'Azerbaiyano',
    LKey.FR: 'azerbaïdjanais',
    LKey.HI: 'आज़रबाइजानी',
    LKey.HU: 'azerbajdzsáni',
    LKey.KO: '아제르바이잔',
    LKey.NE: 'अजरबैजानी',
    LKey.PA: 'ਅਜ਼ਰਬਾਈਜਾਨੀ',
    LKey.RU: 'азербайджанский',
    LKey.TG: 'озарбойҷонӣ',
    LKey.TL: 'Azerbaijani',
    LKey.UR: 'آذربائیجانی',
    LKey.UZ: 'ozarbayjon',
    LKey.ZH: '阿塞拜疆语',
})

#####################################################################################################

_T_GERMAN_MAP: Final = FrozenDict({
    LKey.AR: 'الألمانية',
    LKey.AZ: 'alman',
    LKey.DE: 'Deutsch',
    LKey.EN: 'German',
    LKey.ES: 'Alemán',
    LKey.FR: 'Allemand',
    LKey.HI: 'जर्मन',
    LKey.HU: 'német',
    LKey.KO: '독일 사람',
    LKey.NE: 'जर्मन',
    LKey.PA: 'ਜਰਮਨ',
    LKey.RU: 'немецкий',
    LKey.TG: 'олмонӣ',
    LKey.TL: 'Aleman',
    LKey.UR: 'جرمن',
    LKey.UZ: 'nemis',
    LKey.ZH: '德语',
})

#####################################################################################################

_T_ENGLISH_MAP: Final = FrozenDict({
    LKey.AR: 'إنجليزي',
    LKey.AZ: 'İngilis dili',
    LKey.DE: 'Englisch',
    LKey.EN: 'English',
    LKey.ES: 'Inglés',
    LKey.FR: 'Anglais',
    LKey.HI: 'अंग्रेज़ी',
    LKey.HU: 'angol',
    LKey.KO: '영어',
    LKey.NE: 'अंग्रेजी',
    LKey.PA: 'ਅੰਗਰੇਜ਼ੀ',
    LKey.RU: 'Английский',
    LKey.TG: 'англисӣ',
    LKey.TL: 'Ingles',
    LKey.UR: 'انگریزی',
    LKey.UZ: 'Ingliz',
    LKey.ZH: '英语',
})

#####################################################################################################

_T_SPANISH_MAP: Final = FrozenDict({
    LKey.AR: 'الأسبانية',
    LKey.AZ: 'ispan dili',
    LKey.DE: 'Spanisch',
    LKey.EN: 'Spanish',
    LKey.ES: 'Español',
    LKey.FR: 'Espagnol',
    LKey.HI: 'स्पैनिश',
    LKey.HU: 'spanyol',
    LKey.KO: '스페인 사람',
    LKey.NE: 'स्पेनिस',
    LKey.PA: 'ਸਪੇਨੀ',
    LKey.RU: 'испанский',
    LKey.TG: 'испанӣ',
    LKey.TL: 'Espanyol',
    LKey.UR: 'ہسپانوی',
    LKey.UZ: 'ispancha',
    LKey.ZH: '西班牙语',
})

#####################################################################################################

_T_FRENCH_MAP: Final = FrozenDict({
    LKey.AR: 'فرنسي',
    LKey.AZ: 'fransız',
    LKey.DE: 'Französisch',
    LKey.EN: 'French',
    LKey.ES: 'Francés',
    LKey.FR: 'Français',
    LKey.HI: 'फ्रेंच',
    LKey.HU: 'francia',
    LKey.KO: '프랑스 국민',
    LKey.NE: 'फ्रान्सेली',
    LKey.PA: 'ਫ੍ਰੈਂਚ',
    LKey.RU: 'Французский',
    LKey.TG: 'фаронсавӣ',
    LKey.TL: 'Pranses',
    LKey.UR: 'فرانسیسی',
    LKey.UZ: 'frantsuz',
    LKey.ZH: '法语',
})

#####################################################################################################

_T_HINDI_MAP: Final = FrozenDict({
    LKey.AR: 'الهندية',
    LKey.AZ: 'hind',
    LKey.DE: 'Hindi',
    LKey.EN: 'Hindi',
    LKey.ES: 'hindi',
    LKey.FR: 'hindi',
    LKey.HI: 'हिन्दी',
    LKey.HU: 'hindi',
    LKey.KO: '힌디 어',
    LKey.NE: 'हिन्दी',
    LKey.PA: 'ਹਿੰਦੀ',
    LKey.RU: 'хинди',
    LKey.TG: 'ҳиндӣ',
    LKey.TL: 'Hindi',
    LKey.UR: 'ہندی',
    LKey.UZ: 'hind',
    LKey.ZH: '印地语',
})

#####################################################################################################

_T_KOREAN_MAP: Final = FrozenDict({
    LKey.AR: 'كوري',
    LKey.AZ: 'koreyalı',
    LKey.DE: 'Koreanisch',
    LKey.EN: 'Korean',
    LKey.ES: 'coreano',
    LKey.FR: 'coréen',
    LKey.HI: 'कोरियाई',
    LKey.HU: 'koreai',
    LKey.KO: '한국인',
    LKey.NE: 'कोरियाली',
    LKey.PA: 'ਕੋਰੀਅਨ',
    LKey.RU: 'корейский',
    LKey.TG: 'Корея',
    LKey.TL: 'Koreano',
    LKey.UR: 'کورین',
    LKey.UZ: 'koreys',
    LKey.ZH: '韩国人',
})

#####################################################################################################

_T_NEPALI_MAP: Final = FrozenDict({
    LKey.AR: 'النيبالية',
    LKey.AZ: 'nepal dili',
    LKey.DE: 'Nepalesisch',
    LKey.EN: 'Nepali',
    LKey.ES: 'Nepalí',
    LKey.FR: 'Népalais',
    LKey.HI: 'नेपाली',
    LKey.HU: 'nepáli',
    LKey.KO: '네팔어',
    LKey.NE: 'नेपाली',
    LKey.PA: 'ਨੇਪਾਲੀ',
    LKey.RU: 'непальский',
    LKey.TG: 'непалӣ',
    LKey.TL: 'Nepali',
    LKey.UR: 'نیپالی',
    LKey.UZ: 'Nepal',
    LKey.ZH: '尼泊尔语',
})

#####################################################################################################

_T_RUSSIAN_MAP: Final = FrozenDict({
    LKey.AR: 'الروسية',
    LKey.AZ: 'rus',
    LKey.DE: 'Russisch',
    LKey.EN: 'Russian',
    LKey.ES: 'ruso',
    LKey.FR: 'russe',
    LKey.HI: 'रूसी',
    LKey.HU: 'orosz',
    LKey.KO: '러시아인',
    LKey.NE: 'रुसी',
    LKey.PA: 'ਰੂਸੀ',
    LKey.RU: 'Русский',
    LKey.TG: 'русӣ',
    LKey.TL: 'Ruso',
    LKey.UR: 'روسی',
    LKey.UZ: 'rus',
    LKey.ZH: '俄语',
})

#####################################################################################################

_T_TAJIK_MAP: Final = FrozenDict({
    LKey.AR: 'الطاجيكية',
    LKey.AZ: 'tacik',
    LKey.DE: 'Tadschikisch',
    LKey.EN: 'Tajik',
    LKey.ES: 'Tayiko',
    LKey.FR: 'Tadjik',
    LKey.HI: 'ताजिक',
    LKey.HU: 'tadzsik',
    LKey.KO: '타지크어',
    LKey.NE: 'ताजिक',
    LKey.PA: 'ਤਾਜਿਕ',
    LKey.RU: 'таджикский',
    LKey.TG: 'тоҷикӣ',
    LKey.TL: 'Tajik',
    LKey.UR: 'تاجک',
    LKey.UZ: 'tojik',
    LKey.ZH: '塔吉克',
})

#####################################################################################################

_T_URDU_MAP: Final = FrozenDict({
    LKey.AR: 'الأردية',
    LKey.AZ: 'urdu',
    LKey.DE: 'Urdu',
    LKey.EN: 'Urdu',
    LKey.ES: 'Urdú',
    LKey.FR: 'Ourdou',
    LKey.HI: 'उर्दू',
    LKey.HU: 'urdu',
    LKey.KO: '우르두어',
    LKey.NE: 'उर्दू',
    LKey.PA: 'ਉਰਦੂ',
    LKey.RU: 'урду',
    LKey.TG: 'урду',
    LKey.TL: 'Urdu',
    LKey.UR: 'اردو',
    LKey.UZ: 'urdu',
    LKey.ZH: '乌尔都语',
})

#####################################################################################################

_T_UZBEK_MAP: Final = FrozenDict({
    LKey.AR: 'الأوزبكية',
    LKey.AZ: 'özbək',
    LKey.DE: 'Usbekisch',
    LKey.EN: 'Uzbek',
    LKey.ES: 'Uzbeko',
    LKey.FR: 'Ouzbek',
    LKey.HI: 'उज़बेक',
    LKey.HU: 'üzbég',
    LKey.KO: '우즈베크어',
    LKey.NE: 'उज्बेक',
    LKey.PA: 'ਉਜ਼ਬੇਕ',
    LKey.RU: 'узбекский',
    LKey.TG: 'узбек',
    LKey.TL: 'Uzbek',
    LKey.UR: 'ازبک',
    LKey.UZ: "o'zbek",
    LKey.ZH: '乌兹别克语',
})

#####################################################################################################

_T_CHINESE_MAP: Final = FrozenDict({
    LKey.AR: 'الصينية',
    LKey.AZ: 'çinli',
    LKey.DE: 'chinesisch',
    LKey.EN: 'Chinese',
    LKey.ES: 'Chino',
    LKey.FR: 'Chinois',
    LKey.HI: 'चीनी',
    LKey.HU: 'kínai',
    LKey.KO: '중국인',
    LKey.NE: 'चिनियाँ',
    LKey.PA: 'ਚੀਨੀ',
    LKey.RU: 'китайский',
    LKey.TG: 'чинӣ',
    LKey.TL: 'Intsik',
    LKey.UR: 'چینی',
    LKey.UZ: 'Xitoy',
    LKey.ZH: '中国人',
})

#####################################################################################################

_T_TAGALOG_MAP: Final = FrozenDict({
    LKey.AR: 'التاغالوغية',
    LKey.AZ: 'taqaloq',
    LKey.DE: 'Tagalog',
    LKey.EN: 'Tagalog',
    LKey.ES: 'Tagalo',
    LKey.FR: 'Tagalog',
    LKey.HI: 'तागालोग',
    LKey.HU: 'tagalog',
    LKey.KO: '타갈로그어',
    LKey.NE: 'तागालोग',
    LKey.PA: 'ਤਾਗਾਲੋਗ',
    LKey.RU: 'тагальский',
    LKey.TG: 'Тагалогӣ',
    LKey.TL: 'Tagalog',
    LKey.UR: 'ٹیگالوگ',
    LKey.UZ: 'Tagalog',
    LKey.ZH: '他加禄语',
})

#####################################################################################################

_T_HUNGARIAN_MAP: Final = FrozenDict({
    LKey.AR: 'المجرية',
    LKey.AZ: 'macar',
    LKey.DE: 'ungarisch',
    LKey.EN: 'Hungarian',
    LKey.ES: 'húngaro',
    LKey.FR: 'hongrois',
    LKey.HI: 'हंगेरी',
    LKey.HU: 'magyar',
    LKey.KO: '헝가리 인',
    LKey.NE: 'हंगेरी',
    LKey.PA: 'ਹੰਗੇਰੀਅਨ',
    LKey.RU: 'венгерский',
    LKey.TG: 'Венгрия',
    LKey.TL: 'Hungarian',
    LKey.UR: 'ہنگری',
    LKey.UZ: 'venger',
    LKey.ZH: '匈牙利',
})

#####################################################################################################

_T_PUNJABI_MAP: Final = FrozenDict({
    LKey.AR: 'البنجابية',
    LKey.AZ: 'Pəncabi',
    LKey.DE: 'Punjabi',
    LKey.EN: 'Punjabi',
    LKey.ES: 'punjabi',
    LKey.FR: 'Pendjabi',
    LKey.HI: 'पंजाबी',
    LKey.HU: 'pandzsábi',
    LKey.KO: '펀잡어',
    LKey.NE: 'पञ्जाबी',
    LKey.PA: 'ਪੰਜਾਬੀ',
    LKey.RU: 'пенджаби',
    LKey.TG: 'Панҷобӣ',
    LKey.TL: 'Punjabi',
    LKey.UR: 'پنجابی',
    LKey.UZ: 'panjob',
    LKey.ZH: '旁遮普语',
})

#####################################################################################################

_REC_ERROR_MSG_MAP: Final = FrozenDict({
    LKey.AR: 'فشل التعرف على الكلام. يرجى المحاولة مرة أخرى.',
    LKey.AZ: 'Nitqin tanınması uğursuz oldu. Yenidən cəhd edin.',
    LKey.DE: 'Die Spracherkennung ist fehlgeschlagen. Bitte versuchen Sie es erneut.',
    LKey.EN: 'Speech recognition failed. Please try again.',
    LKey.ES: 'Error en el reconocimiento de voz. Inténtalo de nuevo.',
    LKey.FR: 'La reconnaissance vocale a échoué. Veuillez réessayer.',
    LKey.HI: 'वाक् पहचान विफल. कृपया पुनः प्रयास करें।',
    LKey.HU: 'A beszédfelismerés nem sikerült. Kérjük, próbálja újra.',
    LKey.KO: '음성 인식에 실패했습니다. 다시 시도해 주세요.',
    LKey.NE: 'वाक् पहिचान असफल भयो। कृपया पुन: प्रयास गर्नुहोस्।',
    LKey.PA: 'ਬੋਲੀ ਪਛਾਣ ਅਸਫਲ ਰਹੀ। ਕਿਰਪਾ ਕਰਕੇ ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।',
    LKey.RU: 'Распознавание речи не удалось. Попробуйте еще раз.',
    LKey.TG: 'Шинохтани нутқ ноком шуд. Лутфан бори дигар кӯшиш кунед.',
    LKey.TL: 'Nabigo ang pagkilala sa pagsasalita. Pakisubukang muli.',
    LKey.UR: 'تقریر کی شناخت ناکام ہو گئی۔ براہ کرم دوبارہ کوشش کریں۔',
    LKey.UZ: 'Nutqni tanib bo‘lmadi. Iltimos, qayta urinib koʻring.',
    LKey.ZH: '语音识别失败。请重试。',
})

#####################################################################################################

_LOGIN_MAP: Final = FrozenDict({
    LKey.AR: 'تسجيل الدخول',
    LKey.AZ: 'Daxil ol',
    LKey.DE: 'Login',
    LKey.EN: 'Login',
    LKey.ES: 'Acceso',
    LKey.FR: 'Se connecter',
    LKey.HI: 'लॉग इन करें',
    LKey.HU: 'Bejelentkezés',
    LKey.KO: '로그인',
    LKey.NE: 'लगइन गर्नुहोस्',
    LKey.PA: 'ਲਾਗਿਨ',
    LKey.RU: 'Логин',
    LKey.TG: 'Даромадан',
    LKey.TL: 'Mag-login',
    LKey.UR: 'لاگ ان',
    LKey.UZ: 'Tizimga kirish',
    LKey.ZH: '登录',
})

#####################################################################################################

_PASSWORD_MAP: Final = FrozenDict({
    LKey.AR: 'كلمة المرور',
    LKey.AZ: 'parol',
    LKey.DE: 'Passwort',
    LKey.EN: 'Password',
    LKey.ES: 'Contraseña',
    LKey.FR: 'Mot de passe',
    LKey.HI: 'पासवर्ड',
    LKey.HU: 'Jelszó',
    LKey.KO: '비밀번호',
    LKey.NE: 'पासवर्ड',
    LKey.PA: 'ਪਾਸਵਰਡ',
    LKey.RU: 'Пароль',
    LKey.TG: 'Рамз',
    LKey.TL: 'Password',
    LKey.UR: 'پاس ورڈ',
    LKey.UZ: 'Parol',
    LKey.ZH: '密码',
})

#####################################################################################################

_SIGN_IN_MAP: Final = FrozenDict({
    LKey.AR: 'تسجيل الدخول',
    LKey.AZ: 'Daxil olun',
    LKey.DE: 'anmelden',
    LKey.EN: 'Sign in',
    LKey.ES: 'Iniciar sesión',
    LKey.FR: 'Se connecter',
    LKey.HI: 'दाखिल करना',
    LKey.HU: 'Jelentkezzen be',
    LKey.KO: '로그인',
    LKey.NE: 'साइन इन गर्नुहोस्',
    LKey.PA: 'ਸਾਈਨ - ਇਨ',
    LKey.RU: 'Войти',
    LKey.TG: 'даромад',
    LKey.TL: 'Mag-sign in',
    LKey.UR: 'سائن ان کریں۔',
    LKey.UZ: 'tizimga kirish',
    LKey.ZH: '登入',
})

#####################################################################################################

_ERR_LOGIN_MSG_MAP: Final = FrozenDict({
    LKey.AR: 'تم إدخال تسجيل دخول أو كلمة مرور غير صحيحة',
    LKey.AZ: 'Səhv giriş və ya parol daxil edilib',
    LKey.DE: 'Falscher Login oder falsches Passwort eingegeben',
    LKey.EN: 'Incorrect login or password entered',
    LKey.ES: 'Se ingresó un nombre de usuario o una contraseña incorrectos',
    LKey.FR: 'Login ou mot de passe incorrect saisi',
    LKey.HI: 'गलत लॉगिन या पासवर्ड दर्ज किया गया',
    LKey.HU: 'Helytelen bejelentkezési név vagy jelszó lett megadva',
    LKey.KO: '잘못된 로그인 또는 비밀번호가 입력되었습니다.',
    LKey.NE: 'गलत लगइन वा पासवर्ड प्रविष्ट गरियो',
    LKey.PA: 'ਗਲਤ ਲੌਗਇਨ ਜਾਂ ਪਾਸਵਰਡ ਦਾਖਲ ਕੀਤਾ ਗਿਆ ਹੈ',
    LKey.RU: 'Введен неверный логин или пароль',
    LKey.TG: 'Логин ё парол нодуруст ворид карда шуд',
    LKey.TL: 'Maling login o password ang ipinasok',
    LKey.UR: 'غلط لاگ ان یا پاس ورڈ درج کیا گیا ہے۔',
    LKey.UZ: "Noto'g'ri login yoki parol kiritilgan",
    LKey.ZH: '输入的登录名或密码不正确',
})

_A_NAME_MAP: Final = FrozenDict({
    LKey.AR: 'اسم',
    LKey.AZ: 'ad',
    LKey.DE: 'Name',
    LKey.EN: 'Name',
    LKey.ES: 'Nombre',
    LKey.FR: 'Nom',
    LKey.HI: 'नाम',
    LKey.HU: 'Név',
    LKey.KO: '이름',
    LKey.NE: 'नाम',
    LKey.PA: 'ਨਾਮ',
    LKey.RU: 'Имя',
    LKey.TG: 'Ном',
    LKey.TL: 'Pangalan',
    LKey.UR: 'نام',
    LKey.UZ: 'Ism',
    LKey.ZH: '姓名',
})

#####################################################################################################

_A_ADDRESS_MAP: Final = FrozenDict({
    LKey.AR: 'عنوان',
    LKey.AZ: 'Ünvan',
    LKey.DE: 'Adresse',
    LKey.EN: 'Address',
    LKey.ES: 'DIRECCIÓN',
    LKey.FR: 'Adresse',
    LKey.HI: 'पता',
    LKey.HU: 'Cím',
    LKey.KO: '주소',
    LKey.NE: 'ठेगाना',
    LKey.PA: 'ਪਤਾ',
    LKey.RU: 'Адрес',
    LKey.TG: 'Суроға',
    LKey.TL: 'Address',
    LKey.UR: 'پتہ',
    LKey.UZ: 'Manzil',
    LKey.ZH: '地址',
})

_A_TIME_ZONE_MAP: Final = FrozenDict({
    LKey.AR: 'المنطقة الزمنية',
    LKey.AZ: 'Saat qurşağı',
    LKey.DE: 'Zeitzone',
    LKey.EN: 'Time zone',
    LKey.ES: 'Huso horario',
    LKey.FR: 'Fuseau horaire',
    LKey.HI: 'समय क्षेत्र',
    LKey.HU: 'Időzóna',
    LKey.KO: '시간대',
    LKey.NE: 'समय क्षेत्र',
    LKey.PA: 'ਸਮਾਂ ਖੇਤਰ',
    LKey.RU: 'Часовой пояс',
    LKey.TG: 'Минтақаи вақт',
    LKey.TL: 'Time zone',
    LKey.UR: 'ٹائم زون',
    LKey.UZ: 'Vaqt mintaqasi',
    LKey.ZH: '时区',
})

_A_FULL_NAME_MAP: Final = FrozenDict({
    LKey.AR: 'الاسم الكامل',
    LKey.AZ: 'Tam adı',
    LKey.DE: 'Vollständiger Name',
    LKey.EN: 'Full name',
    LKey.ES: 'Nombre completo',
    LKey.FR: 'Nom et prénom',
    LKey.HI: 'पूरा नाम',
    LKey.HU: 'Teljes név',
    LKey.KO: '전체 이름',
    LKey.NE: 'पूरा नाम',
    LKey.PA: 'ਪੂਰਾ ਨਾਂਮ',
    LKey.RU: 'Полное имя',
    LKey.TG: 'Номи пурра',
    LKey.TL: 'Buong pangalan',
    LKey.UR: 'پورا نام',
    LKey.UZ: "To'liq ism",
    LKey.ZH: '姓名',
})

_A_IS_ACTIVE_MAP: Final = FrozenDict({
    LKey.AR: 'هل هو نشط',
    LKey.AZ: 'Aktivdir',
    LKey.DE: 'Ist aktiv',
    LKey.EN: 'Is active',
    LKey.ES: 'Está activo',
    LKey.FR: 'Est actif',
    LKey.HI: 'सक्रिय है',
    LKey.HU: 'Aktív',
    LKey.KO: '활성화되어 있습니다',
    LKey.NE: 'सक्रिय छ',
    LKey.PA: 'ਸਰਗਰਮ ਹੈ',
    LKey.RU: 'Активен',
    LKey.TG: 'Фаъол аст',
    LKey.TL: 'Ay aktibo',
    LKey.UR: 'فعال ہے۔',
    LKey.UZ: 'Faol',
    LKey.ZH: '处于活动状态',
})

_A_ADMINISTRATOR_MAP: Final = FrozenDict({
    LKey.AR: 'مسؤل',
    LKey.AZ: 'Admin',
    LKey.DE: 'Verwaltung',
    LKey.EN: 'Admin',
    LKey.ES: 'Administración',
    LKey.FR: 'Administrateur',
    LKey.HI: 'एडमिन',
    LKey.HU: 'Admin',
    LKey.KO: '관리자',
    LKey.NE: 'व्यवस्थापक',
    LKey.PA: 'ਐਡਮਿਨ',
    LKey.RU: 'Админ',
    LKey.TG: 'Админ',
    LKey.TL: 'Admin',
    LKey.UR: 'ایڈمن',
    LKey.UZ: 'Admin',
    LKey.ZH: '行政',
})

_A_DEPARTMENT_MAP: Final = FrozenDict({
    LKey.AR: 'قسم',
    LKey.AZ: 'şöbəsi',
    LKey.DE: 'Abteilung',
    LKey.EN: 'Department',
    LKey.ES: 'Departamento',
    LKey.FR: 'Département',
    LKey.HI: 'विभाग',
    LKey.HU: 'Osztály',
    LKey.KO: '부서',
    LKey.NE: 'विभाग',
    LKey.PA: 'ਵਿਭਾਗ',
    LKey.RU: 'Отдел',
    LKey.TG: 'Кафедра',
    LKey.TL: 'Kagawaran',
    LKey.UR: 'محکمہ',
    LKey.UZ: 'Kafedra',
    LKey.ZH: '部门',
})

_A_DEPARTMENT_UUID_MAP: Final = FrozenDict({
    LKey.AR: 'UUID للقسم',
    LKey.AZ: 'Departamentin UUID',
    LKey.DE: 'UUID der Abteilung',
    LKey.EN: 'UUID of Department',
    LKey.ES: 'UUID del Departamento',
    LKey.FR: 'UUID du département',
    LKey.HI: 'विभाग का यूयूआईडी',
    LKey.HU: 'osztály UUID-je',
    LKey.KO: '부서의 UUID',
    LKey.NE: 'विभागको UUID',
    LKey.PA: 'ਵਿਭਾਗ ਦੀ ਯੂ.ਯੂ.ਆਈ.ਡੀ',
    LKey.RU: 'UUID отдела',
    LKey.TG: 'UUID кафедра',
    LKey.TL: 'UUID ng Departamento',
    LKey.UR: 'محکمہ کا UUID',
    LKey.UZ: 'Kafedra UUID',
    LKey.ZH: '部门的 UUID',
})

_A_USER_MAP: Final = FrozenDict({
    LKey.AR: 'مستخدم',
    LKey.AZ: 'İstifadəçi',
    LKey.DE: 'Benutzer',
    LKey.EN: 'User',
    LKey.ES: 'Usuario',
    LKey.FR: 'Utilisateur',
    LKey.HI: 'उपयोगकर्ता',
    LKey.HU: 'Felhasználó',
    LKey.KO: '사용자',
    LKey.NE: 'प्रयोगकर्ता',
    LKey.PA: 'ਉਪਭੋਗਤਾ',
    LKey.RU: 'Пользователь',
    LKey.TG: 'Истифодабаранда',
    LKey.TL: 'Gumagamit',
    LKey.UR: 'صارف',
    LKey.UZ: 'Foydalanuvchi',
    LKey.ZH: '用户',
})

_A_USER_LOGIN_MAP: Final = FrozenDict({
    LKey.AR: 'تسجيل دخول المستخدم',
    LKey.AZ: 'İstifadəçi girişi',
    LKey.DE: 'Benutzeranmeldung',
    LKey.EN: 'User login',
    LKey.ES: 'Inicio de sesión de usuario',
    LKey.FR: 'Connexion utilisateur',
    LKey.HI: 'उपयोगकर्ता लॉगिन',
    LKey.HU: 'Felhasználói bejelentkezés',
    LKey.KO: '사용자 로그인',
    LKey.NE: 'प्रयोगकर्ता लगइन',
    LKey.PA: 'ਉਪਭੋਗਤਾ ਲੌਗਇਨ',
    LKey.RU: 'Логин пользователя',
    LKey.TG: 'Воридшавӣ корбар',
    LKey.TL: 'Login ng user',
    LKey.UR: 'صارف لاگ ان',
    LKey.UZ: 'Foydalanuvchi login',
    LKey.ZH: '用户登录',
})

_A_SESSION_UUID_MAP: Final = FrozenDict({
    LKey.AR: 'معرف الجلسة UUID',
    LKey.AZ: 'Sessiya UUID',
    LKey.DE: 'Sitzungs-UUID',
    LKey.EN: 'Session UUID',
    LKey.ES: 'UUID de sesión',
    LKey.FR: 'UUID de session',
    LKey.HI: 'सत्र UUID',
    LKey.HU: 'Munkamenet UUID',
    LKey.KO: '세션 UUID',
    LKey.NE: 'सत्र UUID',
    LKey.PA: 'ਸੈਸ਼ਨ UUID',
    LKey.RU: 'UUID сеанса',
    LKey.TG: 'Сессия UUID',
    LKey.TL: 'Session UUID',
    LKey.UR: 'سیشن UUID',
    LKey.UZ: 'UUID sessiyasi',
    LKey.ZH: '会话 UUID',
})

_A_DIALOG_UUID_MAP: Final = FrozenDict({
    LKey.AR: 'حوار UUID',
    LKey.AZ: 'Dialoq UUID',
    LKey.DE: 'Dialog-UUID',
    LKey.EN: 'Dialog UUID',
    LKey.ES: 'UUID del cuadro de diálogo',
    LKey.FR: 'UUID de la boîte de dialogue',
    LKey.HI: 'संवाद UUID',
    LKey.HU: 'UUID párbeszédpanel',
    LKey.KO: '대화 UUID',
    LKey.NE: 'संवाद UUID',
    LKey.PA: 'ਡਾਇਲਾਗ UUID',
    LKey.RU: 'UUID диалога',
    LKey.TG: 'Муколамаи UUID',
    LKey.TL: 'Dialog UUID',
    LKey.UR: 'ڈائیلاگ UUID',
    LKey.UZ: 'UUID dialogi',
    LKey.ZH: '对话框 UUID',
})

_A_LANGUAGE_MAP: Final = FrozenDict({
    LKey.AR: 'لغة',
    LKey.AZ: 'Dil',
    LKey.DE: 'Sprache',
    LKey.EN: 'Language',
    LKey.ES: 'Idioma',
    LKey.FR: 'Langue',
    LKey.HI: 'भाषा',
    LKey.HU: 'Nyelv',
    LKey.KO: '언어',
    LKey.NE: 'भाषा',
    LKey.PA: 'ਭਾਸ਼ਾ',
    LKey.RU: 'Язык',
    LKey.TG: 'Забон',
    LKey.TL: 'Wika',
    LKey.UR: 'زبان',
    LKey.UZ: 'Til',
    LKey.ZH: '语言',
})

_A_NPS_SCORE_MAP: Final = FrozenDict({
    LKey.AR: 'نتيجة NPS',
    LKey.AZ: 'NPS hesabı',
    LKey.DE: 'NPS-Wert',
    LKey.EN: 'NPS score',
    LKey.ES: 'Puntuación NPS',
    LKey.FR: 'Score NPS',
    LKey.HI: 'एनपीएस स्कोर',
    LKey.HU: 'NPS pontszám',
    LKey.KO: 'NPS 점수',
    LKey.NE: 'NPS स्कोर',
    LKey.PA: 'NPS ਸਕੋਰ',
    LKey.RU: 'Оценка NPS',
    LKey.TG: 'Натиҷаи NPS',
    LKey.TL: 'marka ng NPS',
    LKey.UR: 'این پی ایس سکور',
    LKey.UZ: 'NPS ball',
    LKey.ZH: 'NPS 评分',
})

_A_TRANSLATION_SCORE_MAP: Final = FrozenDict({
    LKey.AR: 'درجة الترجمة',
    LKey.AZ: 'Tərcümə balı',
    LKey.DE: 'Übersetzungsergebnis',
    LKey.EN: 'Translation score',
    LKey.ES: 'Puntuación de traducción',
    LKey.FR: 'Score de traduction',
    LKey.HI: 'अनुवाद स्कोर',
    LKey.HU: 'Fordítási pontszám',
    LKey.KO: '번역 점수',
    LKey.NE: 'अनुवाद स्कोर',
    LKey.PA: 'ਅਨੁਵਾਦ ਸਕੋਰ',
    LKey.RU: 'Оценка перевода',
    LKey.TG: 'Натиҷаи тарҷума',
    LKey.TL: 'Puntos sa pagsasalin',
    LKey.UR: 'ترجمہ سکور',
    LKey.UZ: 'Tarjima ball',
    LKey.ZH: '翻译分数',
})

_A_USABILITY_SCORE_MAP: Final = FrozenDict({
    LKey.AR: 'درجة قابلية الاستخدام',
    LKey.AZ: 'İstifadə qabiliyyəti balı',
    LKey.DE: 'Benutzerfreundlichkeitsbewertung',
    LKey.EN: 'Usability score',
    LKey.ES: 'Puntuación de usabilidad',
    LKey.FR: "Score d'utilisabilité",
    LKey.HI: 'प्रयोज्यता स्कोर',
    LKey.HU: 'Használhatósági pontszám',
    LKey.KO: '사용성 점수',
    LKey.NE: 'उपयोगिता स्कोर',
    LKey.PA: 'ਉਪਯੋਗਤਾ ਸਕੋਰ',
    LKey.RU: 'Оценка удобства использования',
    LKey.TG: 'Холи қобили истифода',
    LKey.TL: 'Marka ng kakayahang magamit',
    LKey.UR: 'استعمال کا سکور',
    LKey.UZ: 'Foydalanish darajasi',
    LKey.ZH: '可用性评分',
})

_A_DIALOG_START_MAP: Final = FrozenDict({
    LKey.AR: 'بدء الحوار',
    LKey.AZ: 'Dialoq başlanğıcı',
    LKey.DE: 'Dialogstart',
    LKey.EN: 'Dialog start',
    LKey.ES: 'Inicio del diálogo',
    LKey.FR: 'Début du dialogue',
    LKey.HI: 'संवाद प्रारंभ',
    LKey.HU: 'Párbeszéd indítása',
    LKey.KO: '대화 시작',
    LKey.NE: 'संवाद सुरु',
    LKey.PA: 'ਡਾਇਲਾਗ ਸ਼ੁਰੂ',
    LKey.RU: 'Начало диалога',
    LKey.TG: 'Оғози муколама',
    LKey.TL: 'Pagsisimula ng dialog',
    LKey.UR: 'ڈائیلاگ شروع',
    LKey.UZ: 'Dialog boshlanishi',
    LKey.ZH: '对话开始',
})

_A_DIALOG_END_MAP: Final = FrozenDict({
    LKey.AR: 'نهاية الحوار',
    LKey.AZ: 'Dialoqun sonu',
    LKey.DE: 'Dialogende',
    LKey.EN: 'Dialog end',
    LKey.ES: 'Fin del diálogo',
    LKey.FR: 'Fin du dialogue',
    LKey.HI: 'संवाद समाप्त',
    LKey.HU: 'Párbeszéd vége',
    LKey.KO: '대화 종료',
    LKey.NE: 'संवाद अन्त्य',
    LKey.PA: 'ਡਾਇਲਾਗ ਸਮਾਪਤ',
    LKey.RU: 'Конец диалога',
    LKey.TG: 'Анҷоми муколама',
    LKey.TL: 'Katapusan ng dialog',
    LKey.UR: 'ڈائیلاگ اختتام',
    LKey.UZ: 'Dialogning tugashi',
    LKey.ZH: '对话结束',
})

_A_DIALOG_DURATION_MAP: Final = FrozenDict({
    LKey.AR: 'مدة الحوار',
    LKey.AZ: 'Dialoqun müddəti',
    LKey.DE: 'Dauer des Dialogs',
    LKey.EN: 'Duration of dialogue',
    LKey.ES: 'Duración del diálogo',
    LKey.FR: 'Durée du dialogue',
    LKey.HI: 'संवाद की अवधि',
    LKey.HU: 'A párbeszéd időtartama',
    LKey.KO: '대화의 지속 시간',
    LKey.NE: 'संवादको अवधि',
    LKey.PA: 'ਵਾਰਤਾਲਾਪ ਦੀ ਮਿਆਦ',
    LKey.RU: 'Продолжительность диалога',
    LKey.TG: 'Давомнокии муколама',
    LKey.TL: 'Tagal ng dialogue',
    LKey.UR: 'مکالمے کا دورانیہ',
    LKey.UZ: 'Suhbat davomiyligi',
    LKey.ZH: '对话时长',
})

_A_METRIC_MAP: Final = FrozenDict({
    LKey.AR: 'متري',
    LKey.AZ: 'Metrik',
    LKey.DE: 'Metrisch',
    LKey.EN: 'Metric',
    LKey.ES: 'Métrico',
    LKey.FR: 'Métrique',
    LKey.HI: 'मीट्रिक',
    LKey.HU: 'Metrikus',
    LKey.KO: '미터법',
    LKey.NE: 'मेट्रिक',
    LKey.PA: 'ਮੈਟ੍ਰਿਕ',
    LKey.RU: 'Метрика',
    LKey.TG: 'Метрик',
    LKey.TL: 'Sukatan',
    LKey.UR: 'میٹرک',
    LKey.UZ: 'Metrik',
    LKey.ZH: '公制',
})

_A_RESULT_MAP: Final = FrozenDict({
    LKey.AR: 'نتيجة',
    LKey.AZ: 'Nəticə',
    LKey.DE: 'Ergebnis',
    LKey.EN: 'Result',
    LKey.ES: 'Resultado',
    LKey.FR: 'Résultat',
    LKey.HI: 'परिणाम',
    LKey.HU: 'Eredmény',
    LKey.KO: '결과',
    LKey.NE: 'नतिजा',
    LKey.PA: 'ਨਤੀਜਾ',
    LKey.RU: 'Результат',
    LKey.TG: 'Натиҷа',
    LKey.TL: 'Resulta',
    LKey.UR: 'نتیجہ',
    LKey.UZ: 'Natija',
    LKey.ZH: '结果',
})

_A_DESCRIPTION_MAP: Final = FrozenDict({
    LKey.AR: 'وصف',
    LKey.AZ: 'Təsvir',
    LKey.DE: 'Beschreibung',
    LKey.EN: 'Description',
    LKey.ES: 'Descripción',
    LKey.FR: 'Description',
    LKey.HI: 'विवरण',
    LKey.HU: 'Leírás',
    LKey.KO: '설명',
    LKey.NE: 'विवरण',
    LKey.PA: 'ਵਰਣਨ',
    LKey.RU: 'Описание',
    LKey.TG: 'Тавсифи',
    LKey.TL: 'Paglalarawan',
    LKey.UR: 'تفصیل',
    LKey.UZ: 'Tavsif',
    LKey.ZH: '描述',
})

_A_MESSAGE_UUID_MAP: Final = FrozenDict({
    LKey.AR: 'رسالة UUID',
    LKey.AZ: 'Mesaj UUID',
    LKey.DE: 'Nachrichten-UUID',
    LKey.EN: 'Message UUID',
    LKey.ES: 'UUID del mensaje',
    LKey.FR: 'UUID du message',
    LKey.HI: 'संदेश UUID',
    LKey.HU: 'Üzenet UUID',
    LKey.KO: '메시지 UUID',
    LKey.NE: 'सन्देश UUID',
    LKey.PA: 'ਸੁਨੇਹਾ UUID',
    LKey.RU: 'UUID сообщения',
    LKey.TG: 'Паёми UUID',
    LKey.TL: 'Message UUID',
    LKey.UR: 'UUID کو پیغام دیں۔',
    LKey.UZ: 'UUID xabari',
    LKey.ZH: '消息 UUID',
})

_A_CREATION_DATE_MAP: Final = FrozenDict({
    LKey.AR: 'تاريخ الإنشاء',
    LKey.AZ: 'Yaradılma tarixi',
    LKey.DE: 'Erstellungsdatum',
    LKey.EN: 'Date of creation',
    LKey.ES: 'Fecha de creación',
    LKey.FR: 'Date de création',
    LKey.HI: 'निर्माण की तारीख',
    LKey.HU: 'Létrehozás dátuma',
    LKey.KO: '생성일자',
    LKey.NE: 'निर्माण मिति',
    LKey.PA: 'ਰਚਨਾ ਦੀ ਮਿਤੀ',
    LKey.RU: 'Дата создания',
    LKey.TG: 'Санаи офариниш',
    LKey.TL: 'Petsa ng paglikha',
    LKey.UR: 'تخلیق کی تاریخ',
    LKey.UZ: 'Yaratilgan sana',
    LKey.ZH: '创建日期',
})

_A_RECOGNIZED_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'نص معترف به',
    LKey.AZ: 'Tanınmış mətn',
    LKey.DE: 'Erkannter Text',
    LKey.EN: 'Recognized text',
    LKey.ES: 'Texto reconocido',
    LKey.FR: 'Texte reconnu',
    LKey.HI: 'मान्यता प्राप्त पाठ',
    LKey.HU: 'Felismert szöveg',
    LKey.KO: '인식된 텍스트',
    LKey.NE: 'मान्यता प्राप्त पाठ',
    LKey.PA: 'ਮਾਨਤਾ ਪ੍ਰਾਪਤ ਟੈਕਸਟ',
    LKey.RU: 'Распознанный текст',
    LKey.TG: 'Матни эътирофшуда',
    LKey.TL: 'Kinikilalang teksto',
    LKey.UR: 'تسلیم شدہ متن',
    LKey.UZ: 'Taniqli matn',
    LKey.ZH: '已识别的文本',
})

_A_EDITED_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'نص محرر',
    LKey.AZ: 'Redaktə edilmiş mətn',
    LKey.DE: 'Bearbeiteter Text',
    LKey.EN: 'Edited text',
    LKey.ES: 'Texto editado',
    LKey.FR: 'Texte édité',
    LKey.HI: 'संपादित पाठ',
    LKey.HU: 'Szerkesztett szöveg',
    LKey.KO: '편집된 텍스트',
    LKey.NE: 'सम्पादन गरिएको पाठ',
    LKey.PA: 'ਸੰਪਾਦਿਤ ਟੈਕਸਟ',
    LKey.RU: 'Отредактированный текст',
    LKey.TG: 'Матни таҳриршуда',
    LKey.TL: 'Na-edit na teksto',
    LKey.UR: 'ترمیم شدہ متن',
    LKey.UZ: 'Tahrirlangan matn',
    LKey.ZH: '编辑文本',
})

_A_AUDIO_MAP: Final = FrozenDict({
    LKey.AR: 'صوتي',
    LKey.AZ: 'Audio',
    LKey.DE: 'Audio',
    LKey.EN: 'Audio',
    LKey.ES: 'Audio',
    LKey.FR: 'Audio',
    LKey.HI: 'ऑडियो',
    LKey.HU: 'Hang',
    LKey.KO: '오디오',
    LKey.NE: 'अडियो',
    LKey.PA: 'ਆਡੀਓ',
    LKey.RU: 'Аудио',
    LKey.TG: 'Аудио',
    LKey.TL: 'Audio',
    LKey.UR: 'آڈیو',
    LKey.UZ: 'Audio',
    LKey.ZH: '声音的',
})

_A_EDIT_MAP: Final = FrozenDict({
    LKey.AR: 'يحرر',
    LKey.AZ: 'Redaktə et',
    LKey.DE: 'Bearbeiten',
    LKey.EN: 'Edit',
    LKey.ES: 'Editar',
    LKey.FR: 'Modifier',
    LKey.HI: 'संपादन करना',
    LKey.HU: 'Szerkesztés',
    LKey.KO: '편집하다',
    LKey.NE: 'सम्पादन गर्नुहोस्',
    LKey.PA: 'ਸੰਪਾਦਿਤ ਕਰੋ',
    LKey.RU: 'Редактировать',
    LKey.TG: 'Таҳрир',
    LKey.TL: 'I-edit',
    LKey.UR: 'ترمیم کریں۔',
    LKey.UZ: 'Tahrirlash',
    LKey.ZH: '编辑',
})

_A_DELETE_MAP: Final = FrozenDict({
    LKey.AR: 'يمسح',
    LKey.AZ: 'Sil',
    LKey.DE: 'Löschen',
    LKey.EN: 'Delete',
    LKey.ES: 'Borrar',
    LKey.FR: 'Supprimer',
    LKey.HI: 'मिटाना',
    LKey.HU: 'Töröl',
    LKey.KO: '삭제',
    LKey.NE: 'मेट्नुहोस्',
    LKey.PA: 'ਮਿਟਾਓ',
    LKey.RU: 'Удалить',
    LKey.TG: 'Нобуд кунед',
    LKey.TL: 'Tanggalin',
    LKey.UR: 'حذف کریں۔',
    LKey.UZ: 'Oʻchirish',
    LKey.ZH: '删除',
})

_A_CREATE_MAP: Final = FrozenDict({
    LKey.AR: 'يخلق',
    LKey.AZ: 'Yaradın',
    LKey.DE: 'Erstellen',
    LKey.EN: 'Create',
    LKey.ES: 'Crear',
    LKey.FR: 'Créer',
    LKey.HI: 'बनाएं',
    LKey.HU: 'Teremt',
    LKey.KO: '만들다',
    LKey.NE: 'सिर्जना गर्नुहोस्',
    LKey.PA: 'ਬਣਾਓ',
    LKey.RU: 'Создавать',
    LKey.TG: 'Эҷод кунед',
    LKey.TL: 'Lumikha',
    LKey.UR: 'بنائیں',
    LKey.UZ: 'Yaratish',
    LKey.ZH: '创造',
})

_A_FILTER_MAP: Final = FrozenDict({
    LKey.AR: 'فلتر',
    LKey.AZ: 'Filtr',
    LKey.DE: 'Filter',
    LKey.EN: 'Filter',
    LKey.ES: 'Filtrar',
    LKey.FR: 'Filtre',
    LKey.HI: 'फ़िल्टर',
    LKey.HU: 'Szűrő',
    LKey.KO: '필터',
    LKey.NE: 'फिल्टर गर्नुहोस्',
    LKey.PA: 'ਫਿਲਟਰ',
    LKey.RU: 'Фильтр',
    LKey.TG: 'Филтр',
    LKey.TL: 'Salain',
    LKey.UR: 'فلٹر',
    LKey.UZ: 'Filtr',
    LKey.ZH: '筛选',
})

_A_RESET_MAP: Final = FrozenDict({
    LKey.AR: 'إعادة ضبط',
    LKey.AZ: 'Sıfırlayın',
    LKey.DE: 'Zurücksetzen',
    LKey.EN: 'Reset',
    LKey.ES: 'Reiniciar',
    LKey.FR: 'Réinitialiser',
    LKey.HI: 'रीसेट करें',
    LKey.HU: 'Reset',
    LKey.KO: '다시 놓기',
    LKey.NE: 'रिसेट गर्नुहोस्',
    LKey.PA: 'ਰੀਸੈਟ ਕਰੋ',
    LKey.RU: 'Сброс',
    LKey.TG: 'Бозсозӣ',
    LKey.TL: 'I-reset',
    LKey.UR: 'دوبارہ ترتیب دیں۔',
    LKey.UZ: 'Qayta tiklash',
    LKey.ZH: '重置',
})

_A_DOWNLOAD_ALL_MAP: Final = FrozenDict({
    LKey.AR: 'تنزيل الكل',
    LKey.AZ: 'Hamısını yükləyin',
    LKey.DE: 'Alles herunterladen',
    LKey.EN: 'Download all',
    LKey.ES: 'Descargar todo',
    LKey.FR: 'Télécharger tout',
    LKey.HI: 'सभी डाउनलोड करें',
    LKey.HU: 'Az összes letöltése',
    LKey.KO: '모두 다운로드',
    LKey.NE: 'सबै डाउनलोड गर्नुहोस्',
    LKey.PA: 'ਸਾਰੇ ਡਾਊਨਲੋਡ ਕਰੋ',
    LKey.RU: 'Скачать все',
    LKey.TG: 'Ҳама зеркашӣ кунед',
    LKey.TL: 'I-download lahat',
    LKey.UR: 'تمام ڈاؤن لوڈ کریں۔',
    LKey.UZ: 'Hammasini yuklab oling',
    LKey.ZH: '全部下载',
})

_A_SOURCE_LANGUAGE_MAP: Final = FrozenDict({
    LKey.AR: 'اللغة المصدر',
    LKey.AZ: 'Mənbə dili',
    LKey.DE: 'Ausgangssprache',
    LKey.EN: 'Source language',
    LKey.ES: 'Idioma de origen',
    LKey.FR: 'Langue source',
    LKey.HI: 'स्रोत भाषा',
    LKey.HU: 'Forrásnyelv',
    LKey.KO: '소스 언어',
    LKey.NE: 'स्रोत भाषा',
    LKey.PA: 'ਸਰੋਤ ਭਾਸ਼ਾ',
    LKey.RU: 'Исходный язык',
    LKey.TG: 'Забони сарчашма',
    LKey.TL: 'Wikang pinagmulan',
    LKey.UR: 'ماخذ کی زبان',
    LKey.UZ: 'Manba tili',
    LKey.ZH: '源语言',
})

_A_SOURCE_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'النص المصدر',
    LKey.AZ: 'Mənbə mətni',
    LKey.DE: 'Quelltext',
    LKey.EN: 'Source text',
    LKey.ES: 'Texto fuente',
    LKey.FR: 'Texte source',
    LKey.HI: 'स्रोत इबारत',
    LKey.HU: 'Forrás szöveg',
    LKey.KO: '원본 텍스트',
    LKey.NE: 'स्रोत पाठ',
    LKey.PA: 'ਸਰੋਤ ਟੈਕਸਟ',
    LKey.RU: 'Исходный текст',
    LKey.TG: 'Матни манбаъ',
    LKey.TL: 'Pinagmulan ng teksto',
    LKey.UR: 'ماخذ متن',
    LKey.UZ: 'Manba matni',
    LKey.ZH: '源文本',
})

_A_NUMBER_OF_LINES_MAP: Final = FrozenDict({
    LKey.AR: 'عدد الخطوط',
    LKey.AZ: 'Sətirlərin sayı',
    LKey.DE: 'Anzahl der Zeilen',
    LKey.EN: 'Number of lines',
    LKey.ES: 'Número de líneas',
    LKey.FR: 'Nombre de lignes',
    LKey.HI: 'पंक्तियों की संख्या',
    LKey.HU: 'Sorok száma',
    LKey.KO: '줄의 수',
    LKey.NE: 'रेखाहरूको संख्या',
    LKey.PA: 'ਲਾਈਨਾਂ ਦੀ ਸੰਖਿਆ',
    LKey.RU: 'Количество строк',
    LKey.TG: 'Шумораи сатрҳо',
    LKey.TL: 'Bilang ng mga linya',
    LKey.UR: 'لائنوں کی تعداد',
    LKey.UZ: 'Chiziqlar soni',
    LKey.ZH: '行数',
})

_A_TRANSLATION_LANGUAGE_MAP: Final = FrozenDict({
    LKey.AR: 'لغة الترجمة',
    LKey.AZ: 'Tərcümə dili',
    LKey.DE: 'Übersetzungssprache',
    LKey.EN: 'Translation language',
    LKey.ES: 'Idioma de traducción',
    LKey.FR: 'Langue de traduction',
    LKey.HI: 'अनुवाद भाषा',
    LKey.HU: 'Fordítási nyelv',
    LKey.KO: '번역 언어',
    LKey.NE: 'अनुवाद भाषा',
    LKey.PA: 'ਅਨੁਵਾਦ ਭਾਸ਼ਾ',
    LKey.RU: 'Язык перевода',
    LKey.TG: 'Забони тарҷума',
    LKey.TL: 'Wikang pagsasalin',
    LKey.UR: 'ترجمہ کی زبان',
    LKey.UZ: 'Tarjima tili',
    LKey.ZH: '翻译语言',
})

_A_TRANSLATED_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'النص المترجم',
    LKey.AZ: 'Tərcümə edilmiş mətn',
    LKey.DE: 'Übersetzter Text',
    LKey.EN: 'Translated text',
    LKey.ES: 'Texto traducido',
    LKey.FR: 'Texte traduit',
    LKey.HI: 'अनूदित पाठ',
    LKey.HU: 'Lefordított szöveg',
    LKey.KO: '번역된 텍스트',
    LKey.NE: 'अनुवादित पाठ',
    LKey.PA: 'ਅਨੁਵਾਦਿਤ ਟੈਕਸਟ',
    LKey.RU: 'Переведенный текст',
    LKey.TG: 'Матни тарҷумашуда',
    LKey.TL: 'Isinalin ang teksto',
    LKey.UR: 'ترجمہ شدہ متن',
    LKey.UZ: 'Tarjima qilingan matn',
    LKey.ZH: '翻译文本',
})

_A_REFERENCE_TEXT_MAP: Final = FrozenDict({
    LKey.AR: 'نص مرجعي',
    LKey.AZ: 'İstinad mətni',
    LKey.DE: 'Referenztext',
    LKey.EN: 'Reference text',
    LKey.ES: 'Texto de referencia',
    LKey.FR: 'Texte de référence',
    LKey.HI: 'संदर्भ पाठ',
    LKey.HU: 'Referencia szöveg',
    LKey.KO: '참조 텍스트',
    LKey.NE: 'सन्दर्भ पाठ',
    LKey.PA: 'ਹਵਾਲਾ ਪਾਠ',
    LKey.RU: 'Эталонный текст',
    LKey.TG: 'Матни истинод',
    LKey.TL: 'Teksto ng sanggunian',
    LKey.UR: 'حوالہ متن',
    LKey.UZ: 'Malumot matni',
    LKey.ZH: '参考文本',
})

_A_ANOTHER_TRANSLATOR_MAP: Final = FrozenDict({
    LKey.AR: 'مترجم آخر',
    LKey.AZ: 'Başqa bir tərcüməçi',
    LKey.DE: 'Ein anderer Übersetzer',
    LKey.EN: 'Another translator',
    LKey.ES: 'Otro traductor',
    LKey.FR: 'Un autre traducteur',
    LKey.HI: 'एक अन्य अनुवादक',
    LKey.HU: 'Egy másik fordító',
    LKey.KO: '다른 번역가',
    LKey.NE: 'अर्को अनुवादक',
    LKey.PA: 'ਇੱਕ ਹੋਰ ਅਨੁਵਾਦਕ',
    LKey.RU: 'Другой переводчик',
    LKey.TG: 'Дигар тарҷумон',
    LKey.TL: 'Isa pang tagasalin',
    LKey.UR: 'ایک اور مترجم',
    LKey.UZ: 'Boshqa tarjimon',
    LKey.ZH: '另一位翻译',
})

_A_CALCULATE_MAP: Final = FrozenDict({
    LKey.AR: 'احسب',
    LKey.AZ: 'Hesablayın',
    LKey.DE: 'Berechnen',
    LKey.EN: 'Calculate',
    LKey.ES: 'Calcular',
    LKey.FR: 'Calculer',
    LKey.HI: 'गणना',
    LKey.HU: 'Számítsa ki',
    LKey.KO: '믿다',
    LKey.NE: 'गणना गर्नुहोस्',
    LKey.PA: 'ਗਣਨਾ ਕਰੋ',
    LKey.RU: 'Рассчитать',
    LKey.TG: 'Ҳисоб кунед',
    LKey.TL: 'Kalkulahin',
    LKey.UR: 'حساب لگانا',
    LKey.UZ: 'Hisoblash',
    LKey.ZH: '计算',
})

_A_COMPARE_TRANSLATORS_MAP: Final = FrozenDict({
    LKey.AR: 'مقارنة المترجمين',
    LKey.AZ: 'Tərcüməçiləri müqayisə edin',
    LKey.DE: 'Übersetzer vergleichen',
    LKey.EN: 'Compare translators',
    LKey.ES: 'Comparar traductores',
    LKey.FR: 'Comparer les traducteurs',
    LKey.HI: 'अनुवादकों की तुलना करें',
    LKey.HU: 'Hasonlítsa össze a fordítókat',
    LKey.KO: '번역기 비교',
    LKey.NE: 'अनुवादकहरू तुलना गर्नुहोस्',
    LKey.PA: 'ਅਨੁਵਾਦਕਾਂ ਦੀ ਤੁਲਨਾ ਕਰੋ',
    LKey.RU: 'Сравнить переводчиков',
    LKey.TG: 'Тарҷумонҳоро муқоиса кунед',
    LKey.TL: 'Ihambing ang mga tagasalin',
    LKey.UR: 'مترجمین کا موازنہ کریں۔',
    LKey.UZ: 'Tarjimonlarni solishtiring',
    LKey.ZH: '比较译者',
})

_A_RECOGNITION_SCORE_MAP: Final = FrozenDict({
    LKey.AR: 'درجة جودة الاعتراف',
    LKey.AZ: 'Tanınma keyfiyyət balı',
    LKey.DE: 'Qualitätsbewertung der Erkennung',
    LKey.EN: 'Recognition quality score',
    LKey.ES: 'Puntuación de calidad de reconocimiento',
    LKey.FR: 'Score de qualité de reconnaissance',
    LKey.HI: 'मान्यता गुणवत्ता स्कोर',
    LKey.HU: 'Elismerés minőségi pontszáma',
    LKey.KO: '인식 품질 점수',
    LKey.NE: 'पहिचान गुणस्तर स्कोर',
    LKey.PA: 'ਮਾਨਤਾ ਗੁਣਵੱਤਾ ਸਕੋਰ',
    LKey.RU: 'Оценка качества распознавания',
    LKey.TG: 'Нишондиҳандаи сифати эътироф',
    LKey.TL: 'Marka ng kalidad ng pagkilala',
    LKey.UR: 'پہچان کے معیار کا سکور',
    LKey.UZ: 'Tan olish sifati reytingi',
    LKey.ZH: '识别质量得分',
})

_A_DEPARTMENTS_MAP: Final = FrozenDict({
    LKey.AR: 'الأقسام',
    LKey.AZ: 'şöbələri',
    LKey.DE: 'Bereiche',
    LKey.EN: 'Departments',
    LKey.ES: 'Departamentos',
    LKey.FR: 'Départements',
    LKey.HI: 'विभागों',
    LKey.HU: 'Osztályok',
    LKey.KO: '부서',
    LKey.NE: 'विभागहरू',
    LKey.PA: 'ਵਿਭਾਗਾਂ',
    LKey.RU: 'Отделы',
    LKey.TG: 'шуъбахо',
    LKey.TL: 'Mga kagawaran',
    LKey.UR: 'محکمے',
    LKey.UZ: "Bo'limlar",
    LKey.ZH: '部门',
})

_A_USERS_MAP: Final = FrozenDict({
    LKey.AR: 'المستخدمون',
    LKey.AZ: 'İstifadəçilər',
    LKey.DE: 'Benutzer',
    LKey.EN: 'Users',
    LKey.ES: 'Usuarios',
    LKey.FR: 'Utilisateurs',
    LKey.HI: 'उपयोगकर्ताओं',
    LKey.HU: 'Felhasználók',
    LKey.KO: '사용자',
    LKey.NE: 'प्रयोगकर्ताहरू',
    LKey.PA: 'ਉਪਭੋਗਤਾ',
    LKey.RU: 'Пользователи',
    LKey.TG: 'Истифодабарандагон',
    LKey.TL: 'Mga gumagamit',
    LKey.UR: 'صارفین',
    LKey.UZ: 'Foydalanuvchilar',
    LKey.ZH: '用户',
})

_A_DIALOGS_MAP: Final = FrozenDict({
    LKey.AR: 'الحوارات',
    LKey.AZ: 'Dialoqlar',
    LKey.DE: 'Dialoge',
    LKey.EN: 'Dialogs',
    LKey.ES: 'Diálogos',
    LKey.FR: 'Dialogues',
    LKey.HI: 'संवाद',
    LKey.HU: 'Párbeszédek',
    LKey.KO: '대화',
    LKey.NE: 'संवादहरू',
    LKey.PA: 'ਡਾਇਲਾਗ',
    LKey.RU: 'Диалоги',
    LKey.TG: 'Диалогҳо',
    LKey.TL: 'Mga diyalogo',
    LKey.UR: 'ڈائیلاگ',
    LKey.UZ: 'Dialoglar',
    LKey.ZH: '对话',
})

_A_RECOGNITION_ERRORS_MAP: Final = FrozenDict({
    LKey.AR: 'أخطاء التعرف',
    LKey.AZ: 'Tanınma səhvləri',
    LKey.DE: 'Erkennungsfehler',
    LKey.EN: 'Recognition errors',
    LKey.ES: 'Errores de reconocimiento',
    LKey.FR: 'Erreurs de reconnaissance',
    LKey.HI: 'पहचान संबंधी त्रुटियाँ',
    LKey.HU: 'Felismerési hibák',
    LKey.KO: '인식 오류',
    LKey.NE: 'पहिचान त्रुटिहरू',
    LKey.PA: 'ਪਛਾਣ ਦੀਆਂ ਗਲਤੀਆਂ',
    LKey.RU: 'Ошибки распознавания',
    LKey.TG: 'Хатогиҳои эътироф',
    LKey.TL: 'Mga error sa pagkilala',
    LKey.UR: 'شناخت کی غلطیاں',
    LKey.UZ: 'Tanib olish xatolari',
    LKey.ZH: '识别错误',
})

_A_TRANSLATION_METRICS_MAP: Final = FrozenDict({
    LKey.AR: 'مقاييس الترجمة',
    LKey.AZ: 'Tərcümə göstəriciləri',
    LKey.DE: 'Übersetzungsmetriken',
    LKey.EN: 'Translation metrics',
    LKey.ES: 'Métricas de traducción',
    LKey.FR: 'Mesures de traduction',
    LKey.HI: 'अनुवाद मीट्रिक्स',
    LKey.HU: 'Fordítási mutatók',
    LKey.KO: '번역 지표',
    LKey.NE: 'अनुवाद मेट्रिक्स',
    LKey.PA: 'ਅਨੁਵਾਦ ਮਾਪਕ',
    LKey.RU: 'Метрики перевода',
    LKey.TG: 'Метрикҳои тарҷума',
    LKey.TL: 'Mga sukatan ng pagsasalin',
    LKey.UR: 'ترجمہ میٹرکس',
    LKey.UZ: "Tarjima ko'rsatkichlari",
    LKey.ZH: '翻译指标',
})

_A_RECOGNITION_METRICS_MAP: Final = FrozenDict({
    LKey.AR: 'مقاييس الاعتراف',
    LKey.AZ: 'Tanınma Metrikləri',
    LKey.DE: 'Erkennungsmetriken',
    LKey.EN: 'Recognition Metrics',
    LKey.ES: 'Métricas de reconocimiento',
    LKey.FR: 'Mesures de reconnaissance',
    LKey.HI: 'मान्यता मीट्रिक्स',
    LKey.HU: 'Felismerési mérőszámok',
    LKey.KO: '인식 지표',
    LKey.NE: 'पहिचान मेट्रिक्स',
    LKey.PA: 'ਮਾਨਤਾ ਮੈਟ੍ਰਿਕਸ',
    LKey.RU: 'Метрики распознавания',
    LKey.TG: 'Метрикҳои эътироф',
    LKey.TL: 'Mga Sukatan ng Pagkilala',
    LKey.UR: 'شناختی میٹرکس',
    LKey.UZ: "Tan olish ko'rsatkichlari",
    LKey.ZH: '识别指标',
})

_A_DOWNLOAD_MAP: Final = FrozenDict({
    LKey.AR: 'تحميل',
    LKey.AZ: 'Yüklə',
    LKey.DE: 'Herunterladen',
    LKey.EN: 'Download',
    LKey.ES: 'Descargar',
    LKey.FR: 'Télécharger',
    LKey.HI: 'डाउनलोड करना',
    LKey.HU: 'Letöltés',
    LKey.KO: '다운로드',
    LKey.NE: 'डाउनलोड गर्नुहोस्',
    LKey.PA: 'ਡਾਊਨਲੋਡ ਕਰੋ',
    LKey.RU: 'Скачать',
    LKey.TG: 'Зеркашӣ кунед',
    LKey.TL: 'I-download',
    LKey.UR: 'ڈاؤن لوڈ کریں۔',
    LKey.UZ: 'Yuklab oling',
    LKey.ZH: '下载',
})

_THE_USER_MAP: Final = FrozenDict({
    LKey.AR: 'المستخدم',
    LKey.AZ: 'İstifadəçi',
    LKey.DE: 'Der Benutzer',
    LKey.EN: 'The user',
    LKey.ES: 'El usuario',
    LKey.FR: "L'utilisateur",
    LKey.HI: 'प्रयोगकर्ता',
    LKey.HU: 'A felhasználó',
    LKey.KO: '사용자',
    LKey.NE: 'प्रयोगकर्ता',
    LKey.PA: 'ਉਪਭੋਗਤਾ',
    LKey.RU: 'Пользователь',
    LKey.TG: 'Истифодабаранда',
    LKey.TL: 'Ang gumagamit',
    LKey.UR: 'صارف',
    LKey.UZ: 'Foydalanuvchi',
    LKey.ZH: '用户',
})

_HAS_MORE_THAN_ONE_SESSION_MAP: Final = FrozenDict({
    LKey.AR: 'لديه أكثر من جلسة مفتوحة',
    LKey.AZ: 'birdən çox açıq sessiyası var',
    LKey.DE: 'hat mehr als eine offene Sitzung',
    LKey.EN: 'has more than one open session',
    LKey.ES: 'tiene más de una sesión abierta',
    LKey.FR: "a plus d'une session ouverte",
    LKey.HI: 'एक से अधिक खुले सत्र हैं',
    LKey.HU: 'egynél több nyitott munkamenete van',
    LKey.KO: '열려있는 세션이 두 개 이상 있습니다',
    LKey.NE: 'एक भन्दा बढी खुल्ला सत्र छ',
    LKey.PA: 'ਇੱਕ ਤੋਂ ਵੱਧ ਓਪਨ ਸੈਸ਼ਨ ਹਨ',
    LKey.RU: 'имеет более одного открытого сеанса',
    LKey.TG: 'зиёда аз як сессияи кушод дорад',
    LKey.TL: 'ay may higit sa isang bukas na sesyon',
    LKey.UR: 'ایک سے زیادہ کھلے سیشن ہیں۔',
    LKey.UZ: 'bir nechta ochiq sessiyalarga ega',
    LKey.ZH: '有多个打开的会话',
})

_CLOSE_ALL_SESSIONS_MAP: Final = FrozenDict({
    LKey.AR: 'إغلاق الكل باستثناء الحالي',
    LKey.AZ: 'Cari istisna olmaqla, hamısını bağlayın',
    LKey.DE: 'Schließen Sie alle außer dem aktuellen',
    LKey.EN: 'Close all except the current',
    LKey.ES: 'Cerrar todo excepto el actual',
    LKey.FR: "Fermer tout sauf l'actuel",
    LKey.HI: 'वर्तमान को छोड़कर सभी को बंद करें',
    LKey.HU: 'Zárja be az összeset, kivéve az aktuálisat',
    LKey.KO: '현재를 제외한 모든 것을 닫습니다.',
    LKey.NE: 'वर्तमान बाहेक सबै बन्द गर्नुहोस्',
    LKey.PA: 'ਮੌਜੂਦਾ ਨੂੰ ਛੱਡ ਕੇ ਸਭ ਬੰਦ ਕਰੋ',
    LKey.RU: 'Закрыть все, кроме текущего',
    LKey.TG: 'Ҳамаро ба ҷуз ҷорӣ пӯшед',
    LKey.TL: 'Isara ang lahat maliban sa kasalukuyang',
    LKey.UR: 'کرنٹ کے علاوہ سب بند کر دیں۔',
    LKey.UZ: 'Joriydan tashqari hammasini yoping',
    LKey.ZH: '除当前之外关闭所有',
})

_LEAVE_ALL_SESSIONS_OPEN_MAP: Final = FrozenDict({
    LKey.AR: 'اترك جميع الجلسات مفتوحة',
    LKey.AZ: 'Bütün seansları açıq buraxın',
    LKey.DE: 'Alle Sitzungen geöffnet lassen',
    LKey.EN: 'Leave all sessions open',
    LKey.ES: 'Dejar todas las sesiones abiertas',
    LKey.FR: 'Laissez toutes les sessions ouvertes',
    LKey.HI: 'सभी सत्र खुले छोड़ दें',
    LKey.HU: 'Hagyja az összes munkamenetet nyitva',
    LKey.KO: '모든 세션을 열어두세요',
    LKey.NE: 'सबै सत्रहरू खुला छोड्नुहोस्',
    LKey.PA: 'ਸਾਰੇ ਸੈਸ਼ਨਾਂ ਨੂੰ ਖੁੱਲ੍ਹਾ ਛੱਡੋ',
    LKey.RU: 'Оставьте все сессии открытыми',
    LKey.TG: 'Ҳама сессияҳоро кушода гузоред',
    LKey.TL: 'Iwanang bukas ang lahat ng session',
    LKey.UR: 'تمام سیشنز کو کھلا چھوڑ دیں۔',
    LKey.UZ: 'Barcha seanslarni ochiq qoldiring',
    LKey.ZH: '保持所有会话打开',
})

_TOTAL_OPEN_SESSIONS_MAP: Final = FrozenDict({
    LKey.AR: 'مجموع الجلسات المفتوحة',
    LKey.AZ: 'Ümumi açıq sessiyalar',
    LKey.DE: 'Gesamtzahl offener Sitzungen',
    LKey.EN: 'Total open sessions',
    LKey.ES: 'Total de sesiones abiertas',
    LKey.FR: 'Nombre total de séances ouvertes',
    LKey.HI: 'कुल खुले सत्र',
    LKey.HU: 'Összes nyitott munkamenet',
    LKey.KO: '총 오픈 세션',
    LKey.NE: 'कुल खुला सत्रहरू',
    LKey.PA: 'ਕੁੱਲ ਖੁੱਲ੍ਹੇ ਸੈਸ਼ਨ',
    LKey.RU: 'Всего открытых сессий',
    LKey.TG: 'Ҳама сессияҳои кушода',
    LKey.TL: 'Kabuuang bukas na mga session',
    LKey.UR: 'کل کھلے سیشن',
    LKey.UZ: 'Jami ochiq sessiyalar',
    LKey.ZH: '开放会话总数',
})

_LOGIN_TO_YOUR_ACCOUNT_MAP: Final = FrozenDict({
    LKey.AR: 'تسجيل الدخول إلى حسابك',
    LKey.AZ: 'Hesabınıza daxil olun',
    LKey.DE: 'Einloggen auf Ihr Konto',
    LKey.EN: 'Login to your account',
    LKey.ES: 'Inicie sesión en su cuenta',
    LKey.FR: 'Connectez-vous à votre compte',
    LKey.HI: 'अपने अकाउंट में लॉग इन करें',
    LKey.HU: 'Jelentkezzen be fiókjába',
    LKey.KO: '귀하의 계정에 로그인하세요',
    LKey.NE: 'आफ्नो खातामा लगइन गर्नुहोस्',
    LKey.PA: 'ਆਪਣੇ ਖਾਤੇ ਵਿੱਚ ਲੌਗਇਨ ਕਰੋ',
    LKey.RU: 'Войдите в свою учетную запись',
    LKey.TG: 'Ба ҳисоби худ ворид шавед',
    LKey.TL: 'Mag-login sa iyong account',
    LKey.UR: 'اپنے اکاؤنٹ میں لاگ ان کریں۔',
    LKey.UZ: 'Hisobingizga kiring',
    LKey.ZH: '登录您的账户',
})

_A_FROM_MAP: Final = FrozenDict({
    LKey.AR: 'من',
    LKey.AZ: 'From',
    LKey.DE: 'Aus',
    LKey.EN: 'From',
    LKey.ES: 'De',
    LKey.FR: 'Depuis',
    LKey.HI: 'से',
    LKey.HU: 'Tól',
    LKey.KO: '에서',
    LKey.NE: 'बाट',
    LKey.PA: 'ਤੋਂ',
    LKey.RU: 'От',
    LKey.TG: 'Аз',
    LKey.TL: 'Mula sa',
    LKey.UR: 'سے',
    LKey.UZ: 'Kimdan',
    LKey.ZH: '从',
})

_A_TO_MAP: Final = FrozenDict({
    LKey.AR: 'ل',
    LKey.AZ: 'Kimə',
    LKey.DE: 'Zu',
    LKey.EN: 'To',
    LKey.ES: 'A',
    LKey.FR: 'À',
    LKey.HI: 'को',
    LKey.HU: 'To',
    LKey.KO: '에게',
    LKey.NE: 'को',
    LKey.PA: 'ਨੂੰ',
    LKey.RU: 'До',
    LKey.TG: 'Ба',
    LKey.TL: 'Upang',
    LKey.UR: 'کو',
    LKey.UZ: 'Kimga',
    LKey.ZH: '到',
})

_A_ERROR_CREATE_DEP_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ أثناء إنشاء القسم.',
    LKey.AZ: 'Şöbə yaratarkən xəta baş verdi.',
    LKey.DE: 'Fehler beim Erstellen der Abteilung.',
    LKey.EN: 'Error while creating department.',
    LKey.ES: 'Error al crear departamento.',
    LKey.FR: 'Erreur lors de la création du département.',
    LKey.HI: 'विभाग बनाते समय त्रुटि हुई।',
    LKey.HU: 'Hiba az osztály létrehozásakor.',
    LKey.KO: '부서를 생성하는 동안 오류가 발생했습니다.',
    LKey.NE: 'विभाग सिर्जना गर्दा त्रुटि।',
    LKey.PA: 'ਵਿਭਾਗ ਬਣਾਉਣ ਦੌਰਾਨ ਗਲਤੀ।',
    LKey.RU: 'Ошибка при создании отдела.',
    LKey.TG: 'Хатогӣ ҳангоми эҷоди шӯъба.',
    LKey.TL: 'Error habang gumagawa ng departamento.',
    LKey.UR: 'شعبہ بناتے وقت خرابی',
    LKey.UZ: "Bo'lim yaratishda xatolik yuz berdi.",
    LKey.ZH: '创建部门时出错。',
})
_A_ERROR_EDIT_DEP_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ أثناء تحرير القسم.',
    LKey.AZ: 'Şöbəni redaktə edərkən xəta baş verdi.',
    LKey.DE: 'Fehler beim Bearbeiten der Abteilung.',
    LKey.EN: 'Error while editing department.',
    LKey.ES: 'Error al editar el departamento.',
    LKey.FR: "Erreur lors de l'édition du département.",
    LKey.HI: 'विभाग संपादित करते समय त्रुटि हुई।',
    LKey.HU: 'Hiba az osztály szerkesztése közben.',
    LKey.KO: '부서를 편집하는 동안 오류가 발생했습니다.',
    LKey.NE: 'विभाग सम्पादन गर्दा त्रुटि।',
    LKey.PA: 'ਵਿਭਾਗ ਨੂੰ ਸੰਪਾਦਿਤ ਕਰਨ ਦੌਰਾਨ ਗਲਤੀ।',
    LKey.RU: 'Ошибка при редактировании отдела.',
    LKey.TG: 'Хатогӣ ҳангоми таҳрири шӯъба.',
    LKey.TL: 'Error habang nag-e-edit ng departamento.',
    LKey.UR: 'شعبہ میں ترمیم کرتے وقت خرابی',
    LKey.UZ: "Bo'limni tahrirlashda xatolik yuz berdi.",
    LKey.ZH: '编辑部门时出错。',
})
_A_DEP_NAME_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون اسم القسم فارغًا.',
    LKey.AZ: 'Şöbə adı boş ola bilməz.',
    LKey.DE: 'Der Abteilungsname darf nicht leer sein.',
    LKey.EN: 'Department name cannot be empty.',
    LKey.ES: 'El nombre del departamento no puede estar vacío.',
    LKey.FR: 'Le nom du département ne peut pas être vide.',
    LKey.HI: 'विभाग का नाम रिक्त नहीं रह सकता।',
    LKey.HU: 'Az osztály neve nem lehet üres.',
    LKey.KO: '부서 이름은 비워둘 수 없습니다.',
    LKey.NE: 'विभागको नाम खाली हुन सक्दैन।',
    LKey.PA: 'ਵਿਭਾਗ ਦਾ ਨਾਮ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ ਹੈ।',
    LKey.RU: 'Название отдела не может быть пустым.',
    LKey.TG: 'Номи кафедра холӣ буда наметавонад.',
    LKey.TL: 'Hindi maaaring walang laman ang pangalan ng departamento.',
    LKey.UR: 'ڈیپارٹمنٹ کا نام خالی نہیں ہو سکتا۔',
    LKey.UZ: 'Boʻlim nomi boʻsh boʻlishi mumkin emas.',
    LKey.ZH: '部门名称不能为空。',
})
_A_INCORRECT_TIME_ZONE_MAP: Final = FrozenDict({
    LKey.AR: 'تنسيق المنطقة الزمنية غير صالح.',
    LKey.AZ: 'Yanlış saat qurşağı formatı.',
    LKey.DE: 'Ungültiges Zeitzonenformat.',
    LKey.EN: 'Invalid time zone format.',
    LKey.ES: 'Formato de zona horaria no válido.',
    LKey.FR: 'Format de fuseau horaire non valide.',
    LKey.HI: 'अमान्य समय क्षेत्र प्रारूप।',
    LKey.HU: 'Érvénytelen időzóna formátum.',
    LKey.KO: '잘못된 시간대 형식입니다.',
    LKey.NE: 'अमान्य समय क्षेत्र ढाँचा।',
    LKey.PA: 'ਅਵੈਧ ਸਮਾਂ ਖੇਤਰ ਫਾਰਮੈਟ।',
    LKey.RU: 'Неверный формат часового пояса.',
    LKey.TG: 'Формати минтақаи вақт нодуруст аст.',
    LKey.TL: 'Di-wastong format ng time zone.',
    LKey.UR: 'غلط ٹائم زون فارمیٹ۔',
    LKey.UZ: 'Vaqt mintaqasi formati noto‘g‘ri.',
    LKey.ZH: '时区格式无效。',
})
_A_UNABLE_TO_EDIT_MAP: Final = FrozenDict({
    LKey.AR: 'غير قادر على التحرير. لم يتم العثور على القسم.',
    LKey.AZ: 'Redaktə etmək mümkün deyil. Şöbə tapılmadı.',
    LKey.DE: 'Bearbeiten nicht möglich. Abteilung nicht gefunden.',
    LKey.EN: 'Unable to edit. Department not found.',
    LKey.ES: 'No se puede editar. No se encontró el departamento.',
    LKey.FR: 'Impossible de modifier. Département non trouvé.',
    LKey.HI: 'संपादित करने में असमर्थ. विभाग नहीं मिला।',
    LKey.HU: 'Nem lehet szerkeszteni. Az osztály nem található.',
    LKey.KO: '편집할 수 없습니다. 부서를 찾을 수 없습니다.',
    LKey.NE: 'सम्पादन गर्न सकिएन। विभाग फेला परेन।',
    LKey.PA: 'ਸੰਪਾਦਨ ਕਰਨ ਵਿੱਚ ਅਸਮਰੱਥ। ਵਿਭਾਗ ਨਹੀਂ ਮਿਲਿਆ।',
    LKey.RU: 'Невозможно редактировать. Отдел не найден.',
    LKey.TG: 'Таҳрир кардан ғайриимкон аст. Кафедра ёфт нашуд.',
    LKey.TL: 'Hindi ma-edit. Hindi natagpuan ang departamento.',
    LKey.UR: 'ترمیم کرنے سے قاصر۔ محکمہ نہیں ملا۔',
    LKey.UZ: "Tahrirlash imkonsiz. Bo'lim topilmadi.",
    LKey.ZH: '无法编辑。未找到部门。',
})
_A_UNABLE_TO_DELETE_DEP_MAP: Final = FrozenDict({
    LKey.AR: 'من المستحيل حذف قسم لأن المستخدمين مرتبطون به',
    LKey.AZ: 'İstifadəçilər ona bağlı olduğu üçün bölməni silmək mümkün deyil',
    LKey.DE: 'Es ist nicht möglich, eine Abteilung zu löschen, da Benutzer mit ihr verknüpft sind',
    LKey.EN: 'It is impossible to delete a department because users are linked to it',
    LKey.ES: 'Es imposible eliminar un departamento porque los usuarios están vinculados a él.',
    LKey.FR: 'Il est impossible de supprimer un département car des utilisateurs y sont liés',
    LKey.HI: 'किसी विभाग को हटाना असंभव है क्योंकि उपयोगकर्ता उससे जुड़े हुए हैं',
    LKey.HU: 'Lehetetlen törölni egy osztályt, mert a felhasználók hozzá vannak kapcsolva',
    LKey.KO: '사용자가 연결되어 있기 때문에 부서를 삭제할 수 없습니다.',
    LKey.NE: 'डिपार्टमेन्ट मेटाउन असम्भव छ किनभने प्रयोगकर्ताहरू यसमा जोडिएका छन्',
    LKey.PA: 'ਕਿਸੇ ਵਿਭਾਗ ਨੂੰ ਮਿਟਾਉਣਾ ਅਸੰਭਵ ਹੈ ਕਿਉਂਕਿ ਉਪਭੋਗਤਾ ਇਸ ਨਾਲ ਜੁੜੇ ਹੋਏ ਹਨ',
    LKey.RU: 'Невозможно удалить отдел, так как к нему привязаны пользователи.',
    LKey.TG: 'Нобуд кардани шӯъба ғайриимкон аст, зеро корбарон ба он пайванданд',
    LKey.TL: 'Imposibleng magtanggal ng departamento dahil naka-link dito ang mga user',
    LKey.UR: 'کسی شعبہ کو حذف کرنا ناممکن ہے کیونکہ صارفین اس سے منسلک ہیں۔',
    LKey.UZ: "Bo'limni o'chirib bo'lmaydi, chunki foydalanuvchilar unga bog'langan",
    LKey.ZH: '无法删除部门，因为用户与该部门有关联',
})
_A_CANCEL_MAP: Final = FrozenDict({
    LKey.AR: 'يلغي',
    LKey.AZ: 'Ləğv et',
    LKey.DE: 'Stornieren',
    LKey.EN: 'Cancel',
    LKey.ES: 'Cancelar',
    LKey.FR: 'Annuler',
    LKey.HI: 'रद्द करना',
    LKey.HU: 'Mégse',
    LKey.KO: '취소',
    LKey.NE: 'रद्द गर्नुहोस्',
    LKey.PA: 'ਰੱਦ ਕਰੋ',
    LKey.RU: 'Отмена',
    LKey.TG: 'Бекор кардан',
    LKey.TL: 'Kanselahin',
    LKey.UR: 'منسوخ کریں۔',
    LKey.UZ: 'Bekor qilish',
    LKey.ZH: '取消',
})
_A_APPROVE_DELETION_MAP: Final = FrozenDict({
    LKey.AR: 'هل أنت متأكد أنك تريد حذف القسم؟',
    LKey.AZ: 'Şöbəni silmək istədiyinizə əminsiniz',
    LKey.DE: 'Möchten Sie die Abteilung wirklich löschen?',
    LKey.EN: 'Are you sure you want to delete the department',
    LKey.ES: '¿Está seguro de que desea eliminar el departamento?',
    LKey.FR: 'Etes-vous sûr de vouloir supprimer le département',
    LKey.HI: 'क्या आप वाकई विभाग हटाना चाहते हैं',
    LKey.HU: 'Biztosan törli az osztályt?',
    LKey.KO: '부서를 삭제하시겠습니까?',
    LKey.NE: 'के तपाईं विभाग मेटाउन निश्चित हुनुहुन्छ',
    LKey.PA: "ਕੀ ਤੁਸੀਂ ਯਕੀਨੀ ਤੌਰ 'ਤੇ ਵਿਭਾਗ ਨੂੰ ਮਿਟਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ",
    LKey.RU: 'Вы уверены, что хотите удалить отдел?',
    LKey.TG: 'Шумо мутмаин ҳастед, ки мехоҳед кафедраро нест кунед',
    LKey.TL: 'Sigurado ka bang gusto mong tanggalin ang departamento',
    LKey.UR: 'کیا آپ واقعی محکمہ کو حذف کرنا چاہتے ہیں؟',
    LKey.UZ: 'Haqiqatan ham boʻlimni oʻchirib tashlamoqchimisiz',
    LKey.ZH: '您确定要删除该部门吗',
})
_A_YES_MAP: Final = FrozenDict({
    LKey.AR: 'نعم',
    LKey.AZ: 'Bəli',
    LKey.DE: 'Ja',
    LKey.EN: 'Yes',
    LKey.ES: 'Sí',
    LKey.FR: 'Oui',
    LKey.HI: 'हाँ',
    LKey.HU: 'Igen',
    LKey.KO: '예',
    LKey.NE: 'हो',
    LKey.PA: 'ਹਾਂ',
    LKey.RU: 'Да',
    LKey.TG: 'Бале',
    LKey.TL: 'Oo',
    LKey.UR: 'جی ہاں',
    LKey.UZ: 'Ha',
    LKey.ZH: '是的',
})
_A_NO_MAP: Final = FrozenDict({
    LKey.AR: 'لا',
    LKey.AZ: 'yox',
    LKey.DE: 'NEIN',
    LKey.EN: 'No',
    LKey.ES: 'No',
    LKey.FR: 'Non',
    LKey.HI: 'नहीं',
    LKey.HU: 'Nem',
    LKey.KO: '아니요',
    LKey.NE: 'छैन',
    LKey.PA: 'ਨੰ',
    LKey.RU: 'Нет',
    LKey.TG: 'Не',
    LKey.TL: 'Hindi',
    LKey.UR: 'نہیں',
    LKey.UZ: "Yo'q",
    LKey.ZH: '不',
})

_A_ERROR_DELETE_USER_MAP: Final = FrozenDict({
    LKey.AR: 'من غير الممكن حذف مستخدم لأنه يوجد مربعات حوار مرتبطة بهذا المستخدم.',
    LKey.AZ: 'İstifadəçini silmək mümkün deyil, çünki bu istifadəçi ilə əlaqəli dialoqlar var.',
    LKey.DE: 'Das Löschen eines Benutzers ist nicht möglich, da mit diesem Benutzer Dialoge verknüpft sind.',
    LKey.EN: 'It is impossible to delete a user because there are dialogs linked to this user.',
    LKey.ES: 'No es posible eliminar un usuario porque hay cuadros de diálogo vinculados a este usuario.',
    LKey.FR: 'Il est impossible de supprimer un utilisateur car il existe des boîtes de dialogue liées à cet utilisateur.',
    LKey.HI: 'किसी उपयोगकर्ता को हटाना असंभव है, क्योंकि इस उपयोगकर्ता से संवाद जुड़े हुए हैं।',
    LKey.HU: 'Lehetetlen egy felhasználót törölni, mert a felhasználóhoz párbeszédpanelek kapcsolódnak.',
    LKey.KO: '이 사용자와 연결된 대화 상자가 있기 때문에 사용자를 삭제할 수 없습니다.',
    LKey.NE: 'यो प्रयोगकर्तालाई मेटाउन असम्भव छ किनभने त्यहाँ यस प्रयोगकर्तासँग लिङ्क गरिएका संवादहरू छन्।',
    LKey.PA: 'ਕਿਸੇ ਉਪਭੋਗਤਾ ਨੂੰ ਮਿਟਾਉਣਾ ਅਸੰਭਵ ਹੈ ਕਿਉਂਕਿ ਇਸ ਉਪਭੋਗਤਾ ਨਾਲ ਜੁੜੇ ਡਾਇਲਾਗ ਹਨ।',
    LKey.RU: 'Удалить пользователя невозможно, так как с этим пользователем связаны диалоги.',
    LKey.TG: 'Ҳазф кардани корбар ғайриимкон аст, зеро муколамаҳои бо ин корбар алоқаманд мавҷуданд.',
    LKey.TL: 'Imposibleng magtanggal ng user dahil may mga dialog na naka-link sa user na ito.',
    LKey.UR: 'کسی صارف کو حذف کرنا ناممکن ہے کیونکہ اس صارف سے ڈائیلاگ منسلک ہیں۔',
    LKey.UZ: 'Foydalanuvchini oʻchirib boʻlmaydi, chunki bu foydalanuvchi bilan bogʻlangan dialoglar mavjud.',
    LKey.ZH: '无法删除用户，因为有对话框链接到该用户。',
})
_A_ERROR_EDIT_USER_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن التعديل. لم يتم العثور على المستخدم.',
    LKey.AZ: 'Redaktə etmək mümkün deyil. İstifadəçi tapılmadı.',
    LKey.DE: 'Bearbeiten nicht möglich. Benutzer nicht gefunden.',
    LKey.EN: 'Cannot edit. User not found.',
    LKey.ES: 'No se puede editar. No se encontró el usuario.',
    LKey.FR: 'Impossible de modifier. Utilisateur non trouvé.',
    LKey.HI: 'संपादित नहीं किया जा सकता. उपयोगकर्ता नहीं मिला।',
    LKey.HU: 'Nem szerkeszthető. Felhasználó nem található.',
    LKey.KO: '편집할 수 없습니다. 사용자를 찾을 수 없습니다.',
    LKey.NE: 'सम्पादन गर्न सकिँदैन। प्रयोगकर्ता फेला परेन।',
    LKey.PA: 'ਸੰਪਾਦਨ ਨਹੀਂ ਕੀਤਾ ਜਾ ਸਕਦਾ। ਉਪਭੋਗਤਾ ਨਹੀਂ ਮਿਲਿਆ।',
    LKey.RU: 'Невозможно редактировать. Пользователь не найден.',
    LKey.TG: 'Таҳрир кардан мумкин нест. Корбар ёфт нашуд.',
    LKey.TL: 'Hindi makapag-edit. Hindi nahanap ang user.',
    LKey.UR: 'ترمیم نہیں کر سکتے۔ صارف نہیں ملا۔',
    LKey.UZ: 'Tahrirlash imkonsiz. Foydalanuvchi topilmadi.',
    LKey.ZH: '无法编辑。未找到用户。',
})
_A_ERROR_CREATE_USER_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ في إنشاء المستخدم.',
    LKey.AZ: 'İstifadəçi yaratma xətası.',
    LKey.DE: 'Fehler beim Erstellen des Benutzers.',
    LKey.EN: 'Error creating user.',
    LKey.ES: 'Error al crear el usuario.',
    LKey.FR: "Erreur lors de la création de l'utilisateur.",
    LKey.HI: 'उपयोगकर्ता बनाते समय त्रुटि हुई।',
    LKey.HU: 'Hiba történt a felhasználó létrehozásakor.',
    LKey.KO: '사용자 생성 중 오류가 발생했습니다.',
    LKey.NE: 'प्रयोगकर्ता सिर्जना गर्दा त्रुटि।',
    LKey.PA: 'ਉਪਭੋਗਤਾ ਬਣਾਉਣ ਵਿੱਚ ਤਰੁੱਟੀ।',
    LKey.RU: 'Ошибка создания пользователя.',
    LKey.TG: 'Хатогии эҷоди корбар.',
    LKey.TL: 'Error sa paggawa ng user.',
    LKey.UR: 'صارف بنانے میں خرابی۔',
    LKey.UZ: 'Foydalanuvchini yaratishda xatolik yuz berdi.',
    LKey.ZH: '创建用户错误。',
})
_A_CONFIRM_DELETE_USER_MAP: Final = FrozenDict({
    LKey.AR: 'هل أنت متأكد أنك تريد حذف المستخدم؟ ',
    LKey.AZ: 'İstifadəçini silmək istədiyinizə əminsiniz ',
    LKey.DE: 'Möchten Sie den Benutzer wirklich löschen? ',
    LKey.EN: 'Are you sure you want to delete the user ',
    LKey.ES: '¿Estás seguro de que deseas eliminar el usuario? ',
    LKey.FR: "Etes-vous sûr de vouloir supprimer l'utilisateur ",
    LKey.HI: 'क्या आप वाकई उपयोगकर्ता को हटाना चाहते हैं ',
    LKey.HU: 'Biztosan törli a felhasználót? ',
    LKey.KO: '사용자를 삭제하시겠습니까? ',
    LKey.NE: 'के तपाइँ निश्चित हुनुहुन्छ कि तपाइँ प्रयोगकर्ता मेटाउन चाहनुहुन्छ ',
    LKey.PA: "ਕੀ ਤੁਸੀਂ ਯਕੀਨੀ ਤੌਰ 'ਤੇ ਉਪਭੋਗਤਾ ਨੂੰ ਮਿਟਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ ",
    LKey.RU: 'Вы уверены, что хотите удалить пользователя? ',
    LKey.TG: 'Оё мутмаин ҳастед, ки мехоҳед корбарро нест кунед ',
    LKey.TL: 'Sigurado ka bang gusto mong tanggalin ang user ',
    LKey.UR: 'کیا آپ واقعی صارف کو حذف کرنا چاہتے ہیں۔ ',
    LKey.UZ: 'Haqiqatan ham foydalanuvchini oʻchirib tashlamoqchimisiz ',
    LKey.ZH: '您确定要删除该用户吗 ',
})

_A_CLOSE_MAP: Final = FrozenDict({
    LKey.AR: 'يغلق',
    LKey.AZ: 'Bağlayın',
    LKey.DE: 'Schließen',
    LKey.EN: 'Close',
    LKey.ES: 'Cerca',
    LKey.FR: 'Fermer',
    LKey.HI: 'बंद करना',
    LKey.HU: 'Közeli',
    LKey.KO: '닫다',
    LKey.NE: 'बन्द गर्नुहोस्',
    LKey.PA: 'ਬੰਦ ਕਰੋ',
    LKey.RU: 'Закрывать',
    LKey.TG: 'Пӯшед',
    LKey.TL: 'Isara',
    LKey.UR: 'بند',
    LKey.UZ: 'Yopish',
    LKey.ZH: '关闭',
})
_A_REQUIRED_FIELDS_MAP: Final = FrozenDict({
    LKey.AR: 'الحقول مطلوبة.',
    LKey.AZ: 'Sahələr tələb olunur.',
    LKey.DE: 'Felder sind erforderlich.',
    LKey.EN: 'Fields are required.',
    LKey.ES: 'Los campos son obligatorios.',
    LKey.FR: 'Les champs sont obligatoires.',
    LKey.HI: 'फ़ील्ड अनिवार्य हैं।',
    LKey.HU: 'A mezők kitöltése kötelező.',
    LKey.KO: '필수 입력 사항입니다.',
    LKey.NE: 'क्षेत्रहरू आवश्यक छन्।',
    LKey.PA: 'ਖੇਤ ਲੋੜੀਂਦੇ ਹਨ।',
    LKey.RU: 'Поля обязательны для заполнения.',
    LKey.TG: 'Майдонҳо лозиманд.',
    LKey.TL: 'Kinakailangan ang mga patlang.',
    LKey.UR: 'کھیتوں کی ضرورت ہے۔',
    LKey.UZ: 'Maydonlarni kiritish shart.',
    LKey.ZH: '字段是必需的。',
})
_A_WRONG_DATE_FORMAT_MAP: Final = FrozenDict({
    LKey.AR: 'تنسيق التاريخ غير صالح.',
    LKey.AZ: 'Yanlış tarix formatı.',
    LKey.DE: 'Ungültiges Datumsformat.',
    LKey.EN: 'Invalid date format.',
    LKey.ES: 'Formato de fecha no válido.',
    LKey.FR: 'Format de date non valide.',
    LKey.HI: 'अमान्य दिनांक स्वरूप।',
    LKey.HU: 'Érvénytelen dátumformátum.',
    LKey.KO: '날짜 형식이 잘못되었습니다.',
    LKey.NE: 'अमान्य मिति ढाँचा।',
    LKey.PA: 'ਅਵੈਧ ਮਿਤੀ ਫਾਰਮੈਟ।',
    LKey.RU: 'Неверный формат даты.',
    LKey.TG: 'Формати сана нодуруст.',
    LKey.TL: 'Di-wastong format ng petsa.',
    LKey.UR: 'تاریخ کی غلط شکل۔',
    LKey.UZ: 'Sana formati yaroqsiz.',
    LKey.ZH: '日期格式无效。',
})
_A_PASSWORD_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن تكون كلمة المرور فارغة',
    LKey.AZ: 'Parol boş ola bilməz',
    LKey.DE: 'Das Kennwort darf nicht leer sein',
    LKey.EN: 'Password cannot be empty',
    LKey.ES: 'La contraseña no puede estar vacía',
    LKey.FR: 'Le mot de passe ne peut pas être vide',
    LKey.HI: 'पासवर्ड खाली नहीं हो सकता',
    LKey.HU: 'A jelszó nem lehet üres',
    LKey.KO: '비밀번호는 비워둘 수 없습니다.',
    LKey.NE: 'पासवर्ड खाली हुन सक्दैन',
    LKey.PA: 'ਪਾਸਵਰਡ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ',
    LKey.RU: 'Пароль не может быть пустым',
    LKey.TG: 'Рамз холӣ буда наметавонад',
    LKey.TL: 'Hindi maaaring walang laman ang password',
    LKey.UR: 'پاس ورڈ خالی نہیں ہو سکتا',
    LKey.UZ: "Parol bo'sh bo'lishi mumkin emas",
    LKey.ZH: '密码不能为空',
})
_A_LOGIN_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون تسجيل الدخول فارغا',
    LKey.AZ: 'Giriş boş ola bilməz',
    LKey.DE: 'Der Login darf nicht leer sein',
    LKey.EN: 'Login cannot be empty',
    LKey.ES: 'El campo de inicio de sesión no puede estar vacío',
    LKey.FR: 'Le login ne peut pas être vide',
    LKey.HI: 'लॉगिन खाली नहीं हो सकता',
    LKey.HU: 'A bejelentkezési név nem lehet üres',
    LKey.KO: '로그인은 비어있을 수 없습니다',
    LKey.NE: 'लगइन खाली हुन सक्दैन',
    LKey.PA: 'ਲੌਗਇਨ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ',
    LKey.RU: 'Логин не может быть пустым',
    LKey.TG: 'Воридшавӣ холӣ буда наметавонад',
    LKey.TL: 'Hindi maaaring walang laman ang pag-login',
    LKey.UR: 'لاگ ان خالی نہیں ہو سکتا',
    LKey.UZ: "Login bo'sh bo'lishi mumkin emas",
    LKey.ZH: '登录名不能为空',
})
_A_FULL_NAME_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون الاسم الكامل فارغًا',
    LKey.AZ: 'Tam ad boş ola bilməz',
    LKey.DE: 'Der vollständige Name darf nicht leer sein',
    LKey.EN: 'Full name cannot be empty',
    LKey.ES: 'El nombre completo no puede estar vacío',
    LKey.FR: 'Le nom complet ne peut pas être vide',
    LKey.HI: 'पूरा नाम रिक्त नहीं हो सकता',
    LKey.HU: 'A teljes név nem lehet üres',
    LKey.KO: '전체 이름은 비워둘 수 없습니다.',
    LKey.NE: 'पूरा नाम खाली हुन सक्दैन',
    LKey.PA: 'ਪੂਰਾ ਨਾਮ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ ਹੈ',
    LKey.RU: 'Полное имя не может быть пустым',
    LKey.TG: 'Номи пурра наметавонад холӣ бошад',
    LKey.TL: 'Hindi maaaring walang laman ang buong pangalan',
    LKey.UR: 'پورا نام خالی نہیں ہو سکتا',
    LKey.UZ: 'Toʻliq ism boʻsh boʻlishi mumkin emas',
    LKey.ZH: '全名不能为空',
})
_A_SELECT_DEPARTMENT_MAP: Final = FrozenDict({
    LKey.AR: 'اختر القسم',
    LKey.AZ: 'Şöbə seçin',
    LKey.DE: 'Abteilung auswählen',
    LKey.EN: 'Select department',
    LKey.ES: 'Seleccione departamento',
    LKey.FR: 'Sélectionnez un département',
    LKey.HI: 'विभाग चुनें',
    LKey.HU: 'Válasszon osztályt',
    LKey.KO: '부서를 선택하세요',
    LKey.NE: 'विभाग छान्नुहोस्',
    LKey.PA: 'ਵਿਭਾਗ ਚੁਣੋ',
    LKey.RU: 'Выберите отдел',
    LKey.TG: 'Кафедраро интихоб кунед',
    LKey.TL: 'Pumili ng departamento',
    LKey.UR: 'شعبہ منتخب کریں۔',
    LKey.UZ: "Bo'limni tanlang",
    LKey.ZH: '选择部门',
})
_A_NEW_USER_PASSWORD_MAP: Final = FrozenDict({
    LKey.AR: 'كلمة المرور الجديدة',
    LKey.AZ: 'Yeni parol',
    LKey.DE: 'Neues Passwort',
    LKey.EN: 'New password',
    LKey.ES: 'Nueva contraseña',
    LKey.FR: 'Nouveau mot de passe',
    LKey.HI: 'नया पासवर्ड',
    LKey.HU: 'Új jelszó',
    LKey.KO: '새로운 비밀번호',
    LKey.NE: 'नयाँ पासवर्ड',
    LKey.PA: 'ਨਵਾਂ ਪਾਸਵਰਡ',
    LKey.RU: 'Новый пароль',
    LKey.TG: 'Калидвожаи Нав',
    LKey.TL: 'Bagong password',
    LKey.UR: 'نیا پاس ورڈ',
    LKey.UZ: 'Yangi parol',
    LKey.ZH: '新密码',
})
_A_DATE_VALIDATION_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون تاريخ البدء لاحقًا لتاريخ الانتهاء.',
    LKey.AZ: 'Başlama tarixi bitmə tarixindən gec ola bilməz.',
    LKey.DE: 'Das Startdatum kann nicht nach dem Enddatum liegen.',
    LKey.EN: 'The start date cannot be later than the end date.',
    LKey.ES: 'La fecha de inicio no puede ser posterior a la fecha de finalización.',
    LKey.FR: 'La date de début ne peut pas être postérieure à la date de fin.',
    LKey.HI: 'आरंभ तिथि, समाप्ति तिथि से बाद की नहीं हो सकती।',
    LKey.HU: 'A kezdő dátum nem lehet későbbi, mint a befejezés dátuma.',
    LKey.KO: '시작 날짜는 종료 날짜보다 늦을 수 없습니다.',
    LKey.NE: 'सुरु मिति अन्त्य मिति भन्दा पछि हुन सक्दैन।',
    LKey.PA: 'ਸ਼ੁਰੂਆਤੀ ਮਿਤੀ ਸਮਾਪਤੀ ਮਿਤੀ ਤੋਂ ਬਾਅਦ ਦੀ ਨਹੀਂ ਹੋ ਸਕਦੀ।',
    LKey.RU: 'Дата начала не может быть позже даты окончания.',
    LKey.TG: 'Санаи оғоз набояд аз санаи анҷом дертар бошад.',
    LKey.TL: 'Ang petsa ng pagsisimula ay hindi maaaring lumampas sa petsa ng pagtatapos.',
    LKey.UR: 'آغاز کی تاریخ اختتامی تاریخ سے بعد کی نہیں ہو سکتی۔',
    LKey.UZ: "Boshlanish sanasi tugash sanasidan kech bo'lishi mumkin emas.",
    LKey.ZH: '开始日期不能晚于结束日期。',
})
_A_DOWNLOAD_FORMAT_MAP: Final = FrozenDict({
    LKey.AR: 'تنسيق الملف',
    LKey.AZ: 'Fayl formatı',
    LKey.DE: 'Dateiformat',
    LKey.EN: 'File format',
    LKey.ES: 'Formato de archivo',
    LKey.FR: 'Format de fichier',
    LKey.HI: 'फ़ाइल फ़ारमैट',
    LKey.HU: 'Fájlformátum',
    LKey.KO: '파일 형식',
    LKey.NE: 'फाइल ढाँचा',
    LKey.PA: 'ਫਾਈਲ ਫਾਰਮੈਟ',
    LKey.RU: 'Формат файла',
    LKey.TG: 'Формати файл',
    LKey.TL: 'Format ng file',
    LKey.UR: 'فائل کی شکل',
    LKey.UZ: 'Fayl formati',
    LKey.ZH: '文件格式',
})
_A_DOWNLOAD_AUDIO_MAP: Final = FrozenDict({
    LKey.AR: 'تحميل الصوت',
    LKey.AZ: 'Audionu yükləyin',
    LKey.DE: 'Audio herunterladen',
    LKey.EN: 'Download audio',
    LKey.ES: 'Descargar audio',
    LKey.FR: "Télécharger l'audio",
    LKey.HI: 'ऑडियो डाउनलोड करें',
    LKey.HU: 'Hang letöltése',
    LKey.KO: '오디오 다운로드',
    LKey.NE: 'अडियो डाउनलोड गर्नुहोस्',
    LKey.PA: 'ਆਡੀਓ ਡਾਊਨਲੋਡ ਕਰੋ',
    LKey.RU: 'Скачать аудио',
    LKey.TG: 'Зеркашӣ кардани аудио',
    LKey.TL: 'Mag-download ng audio',
    LKey.UR: 'آڈیو ڈاؤن لوڈ کریں۔',
    LKey.UZ: 'Audio yuklab olish',
    LKey.ZH: '下载音频',
})

_M_AVERAGE_MAP: Final = FrozenDict({
    LKey.AR: 'متوسط',
    LKey.AZ: 'orta',
    LKey.DE: 'Durchschnitt',
    LKey.EN: 'average',
    LKey.ES: 'promedio',
    LKey.FR: 'moyenne',
    LKey.HI: 'औसत',
    LKey.HU: 'átlagos',
    LKey.KO: '평균',
    LKey.NE: 'औसत',
    LKey.PA: 'ਔਸਤ',
    LKey.RU: 'средний',
    LKey.TG: 'миёна',
    LKey.TL: 'karaniwan',
    LKey.UR: 'اوسط',
    LKey.UZ: "o'rtacha",
    LKey.ZH: '平均的',
})
_M_AVERAGE_SCORE_MAP: Final = FrozenDict({
    LKey.AR: 'متوسط النتيجة',
    LKey.AZ: 'Orta xal',
    LKey.DE: 'Durchschnittsnote',
    LKey.EN: 'Average score',
    LKey.ES: 'Puntuación media',
    LKey.FR: 'Note moyenne',
    LKey.HI: 'औसत अंक',
    LKey.HU: 'Átlagos pontszám',
    LKey.KO: '평균 점수',
    LKey.NE: 'औसत स्कोर',
    LKey.PA: 'ਔਸਤ ਸਕੋਰ',
    LKey.RU: 'Средний балл',
    LKey.TG: 'Холи миёна',
    LKey.TL: 'Average na marka',
    LKey.UR: 'اوسط سکور',
    LKey.UZ: "O'rtacha ball",
    LKey.ZH: '平均分数',
})
_M_STANDARD_DEVIATION_MAP: Final = FrozenDict({
    LKey.AR: 'الانحراف المعياري',
    LKey.AZ: 'Standart sapma',
    LKey.DE: 'Standardabweichung',
    LKey.EN: 'Standard deviation',
    LKey.ES: 'Desviación estándar',
    LKey.FR: 'Écart type',
    LKey.HI: 'मानक विचलन',
    LKey.HU: 'Szórás',
    LKey.KO: '표준편차',
    LKey.NE: 'मानक विचलन',
    LKey.PA: 'ਮਿਆਰੀ ਵਿਵਹਾਰ',
    LKey.RU: 'Стандартное отклонение',
    LKey.TG: 'Инҳироф стандартӣ',
    LKey.TL: 'Standard deviation',
    LKey.UR: 'معیاری انحراف',
    LKey.UZ: "Standart og'ish",
    LKey.ZH: '标准差',
})
_M_MINIMUM_VALUE_MAP: Final = FrozenDict({
    LKey.AR: 'القيمة الدنيا',
    LKey.AZ: 'Minimum dəyər',
    LKey.DE: 'Mindestwert',
    LKey.EN: 'Minimum value',
    LKey.ES: 'Valor mínimo',
    LKey.FR: 'Valeur minimale',
    LKey.HI: 'न्यूनतम मूल्य',
    LKey.HU: 'Minimális érték',
    LKey.KO: '최소값',
    LKey.NE: 'न्यूनतम मूल्य',
    LKey.PA: 'ਨਿਊਨਤਮ ਮੁੱਲ',
    LKey.RU: 'Минимальное значение',
    LKey.TG: 'Арзиши ҳадди ақал',
    LKey.TL: 'Pinakamababang halaga',
    LKey.UR: 'کم از کم قدر',
    LKey.UZ: 'Minimal qiymat',
    LKey.ZH: '最小值',
})
_M_MAXIMUM_VALUE_MAP: Final = FrozenDict({
    LKey.AR: 'القيمة القصوى',
    LKey.AZ: 'Maksimum dəyər',
    LKey.DE: 'Maximalwert',
    LKey.EN: 'Maximum value',
    LKey.ES: 'Valor máximo',
    LKey.FR: 'Valeur maximale',
    LKey.HI: 'अधिकतम मूल्य',
    LKey.HU: 'Maximális érték',
    LKey.KO: '최대값',
    LKey.NE: 'अधिकतम मान',
    LKey.PA: 'ਅਧਿਕਤਮ ਮੁੱਲ',
    LKey.RU: 'Максимальное значение',
    LKey.TG: 'Арзиши максималӣ',
    LKey.TL: 'Pinakamataas na halaga',
    LKey.UR: 'زیادہ سے زیادہ قدر',
    LKey.UZ: 'Maksimal qiymat',
    LKey.ZH: '最大值',
})
_M_MEDIAN_MAP: Final = FrozenDict({
    LKey.AR: 'متوسط',
    LKey.AZ: 'Median',
    LKey.DE: 'Mittlere',
    LKey.EN: 'Median',
    LKey.ES: 'Mediana',
    LKey.FR: 'Médian',
    LKey.HI: 'मंझला',
    LKey.HU: 'Középső',
    LKey.KO: '중앙값',
    LKey.NE: 'मध्य',
    LKey.PA: 'ਮੱਧਮਾਨ',
    LKey.RU: 'Медиана',
    LKey.TG: 'Миёна',
    LKey.TL: 'Median',
    LKey.UR: 'میڈین',
    LKey.UZ: 'Median',
    LKey.ZH: '中位数',
})
_M_ANOTHER_TRANSLATOR_AVERAGE_MAP: Final = FrozenDict({
    LKey.AR: 'مترجم آخر متوسط',
    LKey.AZ: 'Başqa bir tərcüməçi orta',
    LKey.DE: 'Ein weiterer Übersetzerdurchschnitt',
    LKey.EN: 'Another translator average',
    LKey.ES: 'Otro traductor promedio',
    LKey.FR: 'Un autre traducteur moyen',
    LKey.HI: 'एक अन्य अनुवादक औसत',
    LKey.HU: 'Egy másik fordítói átlag',
    LKey.KO: '다른 번역가 평균',
    LKey.NE: 'अर्को अनुवादक औसत',
    LKey.PA: 'ਇੱਕ ਹੋਰ ਅਨੁਵਾਦਕ ਔਸਤ',
    LKey.RU: 'Другой переводчик в среднем',
    LKey.TG: 'Миёни дигари тарҷумон',
    LKey.TL: 'Isa pang average na tagasalin',
    LKey.UR: 'ایک اور مترجم اوسط',
    LKey.UZ: "Boshqa tarjimon o'rtacha",
    LKey.ZH: '另一位翻译平均',
})
_M_AVERAGE_DIFFERENCE_MAP: Final = FrozenDict({
    LKey.AR: 'متوسط الفرق',
    LKey.AZ: 'Orta fərq',
    LKey.DE: 'Durchschnittliche Differenz',
    LKey.EN: 'Average difference',
    LKey.ES: 'Diferencia media',
    LKey.FR: 'Différence moyenne',
    LKey.HI: 'औसत अंतर',
    LKey.HU: 'Átlagos különbség',
    LKey.KO: '평균 차이',
    LKey.NE: 'औसत भिन्नता',
    LKey.PA: 'ਔਸਤ ਅੰਤਰ',
    LKey.RU: 'Средняя разница',
    LKey.TG: 'Фарқияти миёна',
    LKey.TL: 'Average na pagkakaiba',
    LKey.UR: 'اوسط فرق',
    LKey.UZ: "O'rtacha farq",
    LKey.ZH: '平均差值',
})
_M_CONFIDENCE_INTERVAL_MAP: Final = FrozenDict({
    LKey.AR: 'فاصل الثقة للفرق',
    LKey.AZ: 'Fərqin etibarlılıq intervalı',
    LKey.DE: 'Konfidenzintervall der Differenz',
    LKey.EN: 'Confidence interval of the difference',
    LKey.ES: 'Intervalo de confianza de la diferencia',
    LKey.FR: 'Intervalle de confiance de la différence',
    LKey.HI: 'अंतर का विश्वास अंतराल',
    LKey.HU: 'A különbség bizalmi intervalluma',
    LKey.KO: '차이의 신뢰 구간',
    LKey.NE: 'भिन्नताको आत्मविश्वास अन्तराल',
    LKey.PA: 'ਅੰਤਰ ਦਾ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ',
    LKey.RU: 'Доверительный интервал разницы',
    LKey.TG: 'Фосилаи эътимоди фарқият',
    LKey.TL: 'Agwat ng kumpiyansa ng pagkakaiba',
    LKey.UR: 'فرق کا اعتماد کا وقفہ',
    LKey.UZ: "Farqning ishonch oralig'i",
    LKey.ZH: '差异的置信区间',
})
_M_SIGNIFICANT_DIFFERENCE_MAP: Final = FrozenDict({
    LKey.AR: 'فرق كبير',
    LKey.AZ: 'Əhəmiyyətli fərq',
    LKey.DE: 'Signifikanter Unterschied',
    LKey.EN: 'Significant difference',
    LKey.ES: 'Diferencia significativa',
    LKey.FR: 'Différence significative',
    LKey.HI: 'महत्वपूर्ण अंतर',
    LKey.HU: 'Jelentős különbség',
    LKey.KO: '상당한 차이',
    LKey.NE: 'महत्त्वपूर्ण भिन्नता',
    LKey.PA: 'ਮਹੱਤਵਪੂਰਨ ਅੰਤਰ',
    LKey.RU: 'Существенная разница',
    LKey.TG: 'Фарқияти назаррас',
    LKey.TL: 'Malaking pagkakaiba',
    LKey.UR: 'اہم فرق',
    LKey.UZ: 'Muhim farq',
    LKey.ZH: '显著差异',
})
_M_SELECT_LANG_MAP: Final = FrozenDict({
    LKey.AR: 'اختر اللغة',
    LKey.AZ: 'Dil seçin',
    LKey.DE: 'Sprache auswählen',
    LKey.EN: 'Select language',
    LKey.ES: 'Seleccione idioma',
    LKey.FR: 'Sélectionner la langue',
    LKey.HI: 'भाषा चुने',
    LKey.HU: 'Válasszon nyelvet',
    LKey.KO: '언어 선택',
    LKey.NE: 'भाषा चयन गर्नुहोस्',
    LKey.PA: 'ਭਾਸ਼ਾ ਚੁਣੋ',
    LKey.RU: 'Выберите язык',
    LKey.TG: 'Забонро интихоб кунед',
    LKey.TL: 'Pumili ng wika',
    LKey.UR: 'زبان منتخب کریں۔',
    LKey.UZ: 'Tilni tanlang',
    LKey.ZH: '选择语言',
})
_M_INPUT_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون حقل الإدخال فارغًا.',
    LKey.AZ: 'Daxiletmə sahəsi boş ola bilməz.',
    LKey.DE: 'Das Eingabefeld darf nicht leer sein.',
    LKey.EN: 'The input field cannot be empty.',
    LKey.ES: 'El campo de entrada no puede estar vacío.',
    LKey.FR: 'Le champ de saisie ne peut pas être vide.',
    LKey.HI: 'इनपुट फ़ील्ड रिक्त नहीं रह सकती।',
    LKey.HU: 'A beviteli mező nem lehet üres.',
    LKey.KO: '입력 필드는 비워둘 수 없습니다.',
    LKey.NE: 'इनपुट क्षेत्र खाली हुन सक्दैन।',
    LKey.PA: 'ਇਨਪੁਟ ਖੇਤਰ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ ਹੈ।',
    LKey.RU: 'Поле ввода не может быть пустым.',
    LKey.TG: 'Майдони вуруд холӣ буда наметавонад.',
    LKey.TL: 'Ang input field ay hindi maaaring walang laman.',
    LKey.UR: 'ان پٹ فیلڈ خالی نہیں ہو سکتی۔',
    LKey.UZ: "Kirish maydoni bo'sh bo'lishi mumkin emas.",
    LKey.ZH: '输入字段不能为空。',
})
_M_REFERENCE_EMPTY_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن أن يكون حقل إدخال النص المرجعي فارغًا.',
    LKey.AZ: 'İstinad mətni daxiletmə sahəsi boş ola bilməz.',
    LKey.DE: 'Das Referenztext-Eingabefeld darf nicht leer sein.',
    LKey.EN: 'The reference text input field cannot be empty.',
    LKey.ES: 'El campo de entrada de texto de referencia no puede estar vacío.',
    LKey.FR: 'Le champ de saisie du texte de référence ne peut pas être vide.',
    LKey.HI: 'संदर्भ पाठ इनपुट फ़ील्ड रिक्त नहीं रह सकती।',
    LKey.HU: 'A hivatkozási szövegbeviteli mező nem lehet üres.',
    LKey.KO: '참조 텍스트 입력 필드는 비워둘 수 없습니다.',
    LKey.NE: 'सन्दर्भ पाठ इनपुट क्षेत्र खाली हुन सक्दैन।',
    LKey.PA: 'ਹਵਾਲਾ ਟੈਕਸਟ ਇਨਪੁਟ ਖੇਤਰ ਖਾਲੀ ਨਹੀਂ ਹੋ ਸਕਦਾ ਹੈ।',
    LKey.RU: 'Поле ввода текста ссылки не может быть пустым.',
    LKey.TG: 'Майдони вуруди матни истинод холӣ буда наметавонад.',
    LKey.TL: 'Ang reference na text input field ay hindi maaaring walang laman.',
    LKey.UR: 'حوالہ ٹیکسٹ ان پٹ فیلڈ خالی نہیں ہو سکتا۔',
    LKey.UZ: 'Malumot matnini kiritish maydoni boʻsh boʻlishi mumkin emas.',
    LKey.ZH: '参考文本输入字段不能为空。',
})
_M_DIFFERENT_NUMBER_MAP: Final = FrozenDict({
    LKey.AR: 'عدد مختلف من الأسطر المصدرية والمترجمة.',
    LKey.AZ: 'Müxtəlif mənbə və tərcümə sətirləri.',
    LKey.DE: 'Unterschiedliche Anzahl von Quell- und übersetzten Zeilen.',
    LKey.EN: 'Different number of source and translated lines.',
    LKey.ES: 'Diferente número de líneas fuente y traducidas.',
    LKey.FR: 'Nombre différent de lignes sources et traduites.',
    LKey.HI: 'स्रोत और अनुवादित पंक्तियों की भिन्न संख्या।',
    LKey.HU: 'Különböző számú forrás és lefordított sor.',
    LKey.KO: '소스 줄과 번역된 줄의 수가 다릅니다.',
    LKey.NE: 'स्रोत र अनुवादित लाइनहरूको विभिन्न संख्या।',
    LKey.PA: 'ਸਰੋਤ ਅਤੇ ਅਨੁਵਾਦਿਤ ਲਾਈਨਾਂ ਦੀ ਵੱਖਰੀ ਸੰਖਿਆ।',
    LKey.RU: 'Различное количество исходных и переведенных строк.',
    LKey.TG: 'Шумораи гуногуни манбаъ ва сатрҳои тарҷумашуда.',
    LKey.TL: "Iba't ibang bilang ng pinagmulan at isinalin na mga linya.",
    LKey.UR: 'سورس اور ترجمہ شدہ لائنوں کی مختلف تعداد۔',
    LKey.UZ: 'Turli xil manba va tarjima satrlari.',
    LKey.ZH: '源代码和翻译的行数不同。',
})
_M_REF_DIFFERENT_NUMBER_MAP: Final = FrozenDict({
    LKey.AR: 'عدد الأسطر المرجعية لا يتطابق مع الأصل.',
    LKey.AZ: 'İstinad xətlərinin sayı orijinala uyğun gəlmir.',
    LKey.DE: 'Die Anzahl der Bezugslinien stimmt nicht mit dem Original überein.',
    LKey.EN: 'The number of reference lines does not match the original.',
    LKey.ES: 'El número de líneas de referencia no coincide con el original.',
    LKey.FR: "Le nombre de lignes de référence ne correspond pas à l'original.",
    LKey.HI: 'संदर्भ पंक्तियों की संख्या मूल से मेल नहीं खाती।',
    LKey.HU: 'A hivatkozási sorok száma nem egyezik az eredetivel.',
    LKey.KO: '참조선의 수가 원본과 일치하지 않습니다.',
    LKey.NE: 'सन्दर्भ रेखाहरूको संख्या मूलसँग मेल खाँदैन।',
    LKey.PA: 'ਸੰਦਰਭ ਲਾਈਨਾਂ ਦੀ ਸੰਖਿਆ ਮੂਲ ਨਾਲ ਮੇਲ ਨਹੀਂ ਖਾਂਦੀ।',
    LKey.RU: 'Количество опорных линий не соответствует оригиналу.',
    LKey.TG: 'Шумораи хатҳои истинод ба аслӣ мувофиқат намекунад.',
    LKey.TL: 'Ang bilang ng mga linya ng sanggunian ay hindi tumutugma sa orihinal.',
    LKey.UR: 'حوالہ سطروں کی تعداد اصل سے مماثل نہیں ہے۔',
    LKey.UZ: 'Malumot satrlari soni asl nusxaga mos kelmaydi.',
    LKey.ZH: '參考行數與原文不符。',
})
_M_TRANSLATOR_DIFFERENT_LINES_MAP: Final = FrozenDict({
    LKey.AR: 'عدد أسطر المترجم الآخر لا يتطابق مع العدد الأصلي.',
    LKey.AZ: 'Başqa tərcüməçinin sətirlərinin sayı orijinala uyğun gəlmir.',
    LKey.DE: 'Die Zeilenanzahl eines anderen Übersetzers stimmt nicht mit der des Originals überein.',
    LKey.EN: 'The number of lines of another translator does not match the original one.',
    LKey.ES: 'El número de líneas de otro traductor no coincide con el original.',
    LKey.FR: "Le nombre de lignes d'un autre traducteur ne correspond pas à celui de l'original.",
    LKey.HI: 'दूसरे अनुवादक की पंक्तियों की संख्या मूल अनुवादक से मेल नहीं खाती।',
    LKey.HU: 'Egy másik fordító sorainak száma nem egyezik az eredetivel.',
    LKey.KO: '다른 번역자의 줄 수가 원본과 일치하지 않습니다.',
    LKey.NE: 'अर्को अनुवादकको लाइनहरूको संख्या मूल एकसँग मेल खाँदैन।',
    LKey.PA: 'ਕਿਸੇ ਹੋਰ ਅਨੁਵਾਦਕ ਦੀਆਂ ਲਾਈਨਾਂ ਦੀ ਗਿਣਤੀ ਅਸਲੀ ਨਾਲ ਮੇਲ ਨਹੀਂ ਖਾਂਦੀ।',
    LKey.RU: 'Количество строк другого переводчика не соответствует оригиналу.',
    LKey.TG: 'Миқдори сатрҳои тарҷумони дигар ба сатри аслӣ мувофиқат намекунад.',
    LKey.TL: 'Ang bilang ng mga linya ng isa pang tagasalin ay hindi tumutugma sa orihinal.',
    LKey.UR: 'دوسرے مترجم کی سطروں کی تعداد اصل سے مماثل نہیں ہے۔',
    LKey.UZ: 'Boshqa tarjimonning satrlari soni asl nusxaga mos kelmaydi.',
    LKey.ZH: '另一位译者的行数与原文不符。',
})
_M_TABLE_QUALITY_MAP: Final = FrozenDict({
    LKey.AR: 'جدول نتائج تقييم جودة الترجمة.',
    LKey.AZ: 'Tərcümə keyfiyyətinin qiymətləndirilməsi nəticələri cədvəli.',
    LKey.DE: 'Tabelle mit den Ergebnissen der Bewertung der Übersetzungsqualität.',
    LKey.EN: 'Translation quality assessment results table.',
    LKey.ES: 'Tabla de resultados de la evaluación de la calidad de la traducción.',
    LKey.FR: 'Tableau des résultats de l’évaluation de la qualité de la traduction.',
    LKey.HI: 'अनुवाद गुणवत्ता मूल्यांकन परिणाम तालिका।',
    LKey.HU: 'Fordítási minőségértékelés eredménytáblázata.',
    LKey.KO: '번역 품질 평가 결과표.',
    LKey.NE: 'अनुवाद गुणस्तर मूल्याङ्कन परिणाम तालिका।',
    LKey.PA: 'ਅਨੁਵਾਦ ਗੁਣਵੱਤਾ ਮੁਲਾਂਕਣ ਨਤੀਜੇ ਸਾਰਣੀ।',
    LKey.RU: 'Таблица результатов оценки качества перевода.',
    LKey.TG: 'Ҷадвали натиҷаҳои арзёбии сифати тарҷума.',
    LKey.TL: 'Talaan ng mga resulta ng pagtatasa ng kalidad ng pagsasalin.',
    LKey.UR: 'ترجمہ کے معیار کی تشخیص کے نتائج کا جدول۔',
    LKey.UZ: 'Tarjima sifatini baholash natijalari jadvali.',
    LKey.ZH: '翻译质量评估结果表。',
})
_M_METRICS_COMPLETED_MAP: Final = FrozenDict({
    LKey.AR: 'تم الانتهاء من تقييم جودة الترجمة.',
    LKey.AZ: 'Tərcümə keyfiyyətinin qiymətləndirilməsi tamamlandı.',
    LKey.DE: 'Bewertung der Übersetzungsqualität abgeschlossen.',
    LKey.EN: 'Translation quality assessment completed.',
    LKey.ES: 'Evaluación de la calidad de la traducción completada.',
    LKey.FR: 'Évaluation de la qualité de la traduction terminée.',
    LKey.HI: 'अनुवाद गुणवत्ता मूल्यांकन पूरा हुआ।',
    LKey.HU: 'A fordítási minőség felmérése befejeződött.',
    LKey.KO: '번역 품질 평가가 완료되었습니다.',
    LKey.NE: 'अनुवाद गुणस्तर मूल्याङ्कन पूरा भयो।',
    LKey.PA: 'ਅਨੁਵਾਦ ਗੁਣਵੱਤਾ ਮੁਲਾਂਕਣ ਪੂਰਾ ਹੋਇਆ।',
    LKey.RU: 'Оценка качества перевода завершена.',
    LKey.TG: 'Арзёбии сифати тарҷума анҷом ёфт.',
    LKey.TL: 'Nakumpleto ang pagtatasa ng kalidad ng pagsasalin.',
    LKey.UR: 'ترجمہ کے معیار کا جائزہ مکمل ہو گیا۔',
    LKey.UZ: 'Tarjima sifatini baholash yakunlandi.',
    LKey.ZH: '翻译质量评估已完成。',
})
_M_METRICS_ERROR_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ في تقييم جودة الترجمة.',
    LKey.AZ: 'Tərcümə keyfiyyətinin qiymətləndirilməsi xətası.',
    LKey.DE: 'Fehler bei der Bewertung der Übersetzungsqualität.',
    LKey.EN: 'Translation quality assessment error.',
    LKey.ES: 'Error en la evaluación de la calidad de la traducción.',
    LKey.FR: 'Erreur d’évaluation de la qualité de la traduction.',
    LKey.HI: 'अनुवाद गुणवत्ता मूल्यांकन त्रुटि।',
    LKey.HU: 'Fordítási minőségértékelési hiba.',
    LKey.KO: '번역 품질 평가 오류.',
    LKey.NE: 'अनुवाद गुणस्तर मूल्याङ्कन त्रुटि।',
    LKey.PA: 'ਅਨੁਵਾਦ ਗੁਣਵੱਤਾ ਮੁਲਾਂਕਣ ਗਲਤੀ।',
    LKey.RU: 'Ошибка оценки качества перевода.',
    LKey.TG: 'Хатогии арзёбии сифати тарҷума.',
    LKey.TL: 'Error sa pagtatasa ng kalidad ng pagsasalin.',
    LKey.UR: 'ترجمہ کے معیار کی تشخیص کی غلطی۔',
    LKey.UZ: 'Tarjima sifatini baholash xatosi.',
    LKey.ZH: '翻译质量评估错误。',
})
_M_WIP_MAP: Final = FrozenDict({
    LKey.AR: 'يعرض المقياس النسبة المئوية للمعلومات المحفوظة في النص المعترف به.',
    LKey.AZ: 'Metrik tanınan mətndə saxlanan məlumatın faizini göstərir.',
    LKey.DE: 'Die Metrik zeigt den Prozentsatz der Informationen, die im erkannten Text gespeichert sind.',
    LKey.EN: 'The metric shows the percentage of information saved in the recognized text.',
    LKey.ES: 'La métrica muestra el porcentaje de información guardada en el texto reconocido.',
    LKey.FR: "La métrique montre le pourcentage d'informations enregistrées dans le texte reconnu.",
    LKey.HI: 'यह मीट्रिक पहचाने गए पाठ में सहेजी गई जानकारी का प्रतिशत दर्शाता है।',
    LKey.HU: 'A mérőszám a felismert szövegben elmentett információk százalékos arányát mutatja.',
    LKey.KO: '이 지표는 인식된 텍스트에 저장된 정보의 비율을 보여줍니다.',
    LKey.NE: 'मेट्रिकले मान्यता प्राप्त पाठमा सुरक्षित गरिएको जानकारीको प्रतिशत देखाउँछ।',
    LKey.PA: 'ਮੈਟ੍ਰਿਕ ਮਾਨਤਾ ਪ੍ਰਾਪਤ ਟੈਕਸਟ ਵਿੱਚ ਸੁਰੱਖਿਅਤ ਕੀਤੀ ਜਾਣਕਾਰੀ ਦੀ ਪ੍ਰਤੀਸ਼ਤਤਾ ਦਿਖਾਉਂਦਾ ਹੈ।',
    LKey.RU: 'Метрика показывает процент информации, сохраненной в распознанном тексте.',
    LKey.TG: 'Метрик фоизи иттилоотро дар матни эътирофшуда нишон медиҳад.',
    LKey.TL: 'Ipinapakita ng sukatan ang porsyento ng impormasyong na-save sa kinikilalang teksto.',
    LKey.UR: 'میٹرک تسلیم شدہ متن میں محفوظ کردہ معلومات کا فیصد دکھاتا ہے۔',
    LKey.UZ: "Ko'rsatkich tan olingan matnda saqlangan ma'lumotlarning foizini ko'rsatadi.",
    LKey.ZH: '该指标显示的是识别文本中保存的信息百分比。',
})
_M_WIL_MAP: Final = FrozenDict({
    LKey.AR: 'يُظهر المقياس النسبة المئوية للمعلومات المفقودة في النص المعترف به.',
    LKey.AZ: 'Metrik tanınan mətndə itirilmiş məlumatın faizini göstərir.',
    LKey.DE: 'Die Metrik zeigt den Prozentsatz verlorener Informationen im erkannten Text.',
    LKey.EN: 'The metric shows the percentage of lost information in the recognized text.',
    LKey.ES: 'La métrica muestra el porcentaje de información perdida en el texto reconocido.',
    LKey.FR: "La métrique montre le pourcentage d'informations perdues dans le texte reconnu.",
    LKey.HI: 'यह मीट्रिक पहचाने गए पाठ में खोई गई जानकारी का प्रतिशत दर्शाता है।',
    LKey.HU: 'A mérőszám az elveszett információ százalékos arányát mutatja a felismert szövegben.',
    LKey.KO: '이 지표는 인식된 텍스트에서 손실된 정보의 비율을 보여줍니다.',
    LKey.NE: 'मेट्रिकले मान्यता प्राप्त पाठमा हराएको जानकारीको प्रतिशत देखाउँछ।',
    LKey.PA: 'ਮੈਟ੍ਰਿਕ ਮਾਨਤਾ ਪ੍ਰਾਪਤ ਟੈਕਸਟ ਵਿੱਚ ਗੁੰਮ ਹੋਈ ਜਾਣਕਾਰੀ ਦੀ ਪ੍ਰਤੀਸ਼ਤਤਾ ਦਿਖਾਉਂਦਾ ਹੈ।',
    LKey.RU: 'Метрика показывает процент потерянной информации в распознанном тексте.',
    LKey.TG: 'Метрик фоизи маълумоти гумшударо дар матни эътирофшуда нишон медиҳад.',
    LKey.TL: 'Ipinapakita ng sukatan ang porsyento ng nawalang impormasyon sa kinikilalang teksto.',
    LKey.UR: 'میٹرک تسلیم شدہ متن میں گم شدہ معلومات کا فیصد دکھاتا ہے۔',
    LKey.UZ: "Ko'rsatkich tan olingan matndagi yo'qolgan ma'lumotlarning foizini ko'rsatadi.",
    LKey.ZH: '该指标显示的是识别文本中丢失信息的百分比。',
})
_M_WER_MAP: Final = FrozenDict({
    LKey.AR: 'نسبة الأخطاء في التعرف على الكلمات.',
    LKey.AZ: 'Sözün tanınmasında səhvlərin faizi.',
    LKey.DE: 'Prozentsatz der Fehler bei der Worterkennung.',
    LKey.EN: 'Percentage of errors in word recognition.',
    LKey.ES: 'Porcentaje de errores en el reconocimiento de palabras.',
    LKey.FR: "Pourcentage d'erreurs dans la reconnaissance des mots.",
    LKey.HI: 'शब्द पहचान में त्रुटियों का प्रतिशत।',
    LKey.HU: 'A szófelismerés hibáinak százalékos aránya.',
    LKey.KO: '단어 인식 오류율.',
    LKey.NE: 'शब्द पहिचानमा त्रुटिहरूको प्रतिशत।',
    LKey.PA: 'ਸ਼ਬਦ ਪਛਾਣ ਵਿੱਚ ਗਲਤੀਆਂ ਦੀ ਪ੍ਰਤੀਸ਼ਤਤਾ।',
    LKey.RU: 'Процент ошибок при распознавании слов.',
    LKey.TG: 'Фоизи хатогиҳо дар шинохти калима.',
    LKey.TL: 'Porsiyento ng mga pagkakamali sa pagkilala ng salita.',
    LKey.UR: 'لفظ کی شناخت میں غلطیوں کا فیصد۔',
    LKey.UZ: "So'zni aniqlashdagi xatolar foizi.",
    LKey.ZH: '单词识别的错误百分比。',
})
_M_MER_MAP: Final = FrozenDict({
    LKey.AR: 'تعديل لـ WER حيث تتم ملاحظة الاستبدالات والإدخالات فقط.',
    LKey.AZ: 'Yalnız əvəzetmələrin və əlavələrin müşahidə edildiyi WER modifikasiyası.',
    LKey.DE: 'Eine Modifikation von WER, bei der nur Substitutionen und Einfügungen beobachtet werden.',
    LKey.EN: 'A modification of WER where only substitutions and insertions are observed.',
    LKey.ES: 'Una modificación de WER donde solo se observan sustituciones e inserciones.',
    LKey.FR: 'Une modification du WER où seules les substitutions et les insertions sont observées.',
    LKey.HI: 'WER का एक संशोधन जहां केवल प्रतिस्थापन और सम्मिलन देखे जाते हैं।',
    LKey.HU: 'A WER olyan módosítása, ahol csak szubsztitúciók és inszerciók figyelhetők meg.',
    LKey.KO: '대체와 삽입만 관찰되는 WER의 수정판입니다.',
    LKey.NE: 'WER को परिमार्जन जहाँ केवल प्रतिस्थापन र सम्मिलनहरू अवलोकन गरिन्छ।',
    LKey.PA: 'WER ਦੀ ਇੱਕ ਸੋਧ ਜਿੱਥੇ ਸਿਰਫ਼ ਬਦਲ ਅਤੇ ਸੰਮਿਲਨ ਦੇਖੇ ਜਾਂਦੇ ਹਨ।',
    LKey.RU: 'Модификация WER, в которой наблюдаются только замены и вставки.',
    LKey.TG: 'Тағироти WER, ки танҳо ивазкунӣ ва воридкунӣ мушоҳида мешавад.',
    LKey.TL: 'Isang pagbabago ng WER kung saan ang mga pagpapalit at pagsingit lamang ang sinusunod.',
    LKey.UR: 'WER کی ایک ترمیم جہاں صرف متبادلات اور اضافے کا مشاہدہ کیا جاتا ہے۔',
    LKey.UZ: 'WER modifikatsiyasi, bunda faqat almashtirishlar va kiritishlar kuzatiladi.',
    LKey.ZH: 'WER 的修改版，其中仅观察到替换和插入。',
})
_M_CER_MAP: Final = FrozenDict({
    LKey.AR: 'مماثل لـ WER، لكنه ينطبق على الأحرف بدلاً من الكلمات.',
    LKey.AZ: 'WER-ə bənzəyir, lakin sözlər əvəzinə simvollara aiddir.',
    LKey.DE: 'Ähnlich wie WER, gilt jedoch für Zeichen statt für Wörter.',
    LKey.EN: 'Similar to WER, but applies to characters instead of words.',
    LKey.ES: 'Similar a WER, pero se aplica a caracteres en lugar de palabras.',
    LKey.FR: "Similaire à WER, mais s'applique aux caractères plutôt qu'aux mots.",
    LKey.HI: 'WER के समान, लेकिन शब्दों के बजाय वर्णों पर लागू होता है।',
    LKey.HU: 'Hasonló a WER-hez, de szavak helyett karakterekre vonatkozik.',
    LKey.KO: 'WER과 유사하지만 단어가 아닌 문자에 적용됩니다.',
    LKey.NE: 'WER जस्तै, तर शब्दहरूको सट्टा वर्णहरूमा लागू हुन्छ।',
    LKey.PA: "WER ਦੇ ਸਮਾਨ, ਪਰ ਸ਼ਬਦਾਂ ਦੀ ਬਜਾਏ ਅੱਖਰਾਂ 'ਤੇ ਲਾਗੂ ਹੁੰਦਾ ਹੈ।",
    LKey.RU: 'Аналогично WER, но применяется к символам, а не к словам.',
    LKey.TG: 'Ба WER монанд аст, аммо ба ҷои калимаҳо ба аломатҳо дахл дорад.',
    LKey.TL: 'Katulad ng WER, ngunit nalalapat sa mga character sa halip na mga salita.',
    LKey.UR: 'WER کی طرح، لیکن الفاظ کے بجائے حروف پر لاگو ہوتا ہے۔',
    LKey.UZ: "WER ga o'xshash, lekin so'zlar o'rniga belgilar uchun amal qiladi.",
    LKey.ZH: '与 WER 类似，但适用于字符而不是单词。',
})
_M_JER_MAP: Final = FrozenDict({
    LKey.AR: 'مقياس يعتمد على مسافة جاكارد.',
    LKey.AZ: 'Jaccard məsafəsinə əsaslanan metrik.',
    LKey.DE: 'Eine Metrik basierend auf der Jaccard-Distanz.',
    LKey.EN: 'A metric based on the Jaccard distance.',
    LKey.ES: 'Una métrica basada en la distancia Jaccard.',
    LKey.FR: 'Une mesure basée sur la distance de Jaccard.',
    LKey.HI: 'जैकार्ड दूरी पर आधारित एक मीट्रिक।',
    LKey.HU: 'A Jaccard távolságon alapuló mérőszám.',
    LKey.KO: '자카드 거리를 기반으로 한 지표.',
    LKey.NE: 'Jaccard दूरीमा आधारित मेट्रिक।',
    LKey.PA: "ਜੈਕਾਰਡ ਦੂਰੀ 'ਤੇ ਆਧਾਰਿਤ ਇੱਕ ਮੈਟ੍ਰਿਕ।",
    LKey.RU: 'Метрика, основанная на расстоянии Жаккара.',
    LKey.TG: 'Метрик дар асоси масофаи Жаккард.',
    LKey.TL: 'Isang sukatan batay sa distansya ng Jaccard.',
    LKey.UR: 'جیکارڈ فاصلے پر مبنی ایک میٹرک۔',
    LKey.UZ: "Jaccard masofasiga asoslangan ko'rsatkich.",
    LKey.ZH: '基于杰卡德距离的度量。',
})
_M_RECOGNITION_ERROR_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ في حساب مقاييس التعرف',
    LKey.AZ: 'Tanınma metriklərinin hesablanması xətası',
    LKey.DE: 'Fehler bei der Berechnung der Erkennungsmetriken',
    LKey.EN: 'Error calculating recognition metrics',
    LKey.ES: 'Error al calcular las métricas de reconocimiento',
    LKey.FR: 'Erreur lors du calcul des mesures de reconnaissance',
    LKey.HI: 'मान्यता मीट्रिक की गणना करते समय त्रुटि',
    LKey.HU: 'Hiba a felismerési mutatók kiszámításakor',
    LKey.KO: '인식 지표 계산 오류',
    LKey.NE: 'पहिचान मेट्रिक्स गणना गर्दा त्रुटि',
    LKey.PA: 'ਮਾਨਤਾ ਮੈਟ੍ਰਿਕਸ ਦੀ ਗਣਨਾ ਕਰਨ ਵਿੱਚ ਤਰੁੱਟੀ',
    LKey.RU: 'Ошибка расчета показателей распознавания',
    LKey.TG: 'Хатогӣ ҳангоми ҳисоб кардани ченакҳои шинохтан',
    LKey.TL: 'Error sa pagkalkula ng mga sukatan ng pagkilala',
    LKey.UR: 'شناختی میٹرکس کا حساب لگانے میں خرابی۔',
    LKey.UZ: 'Tanib olish ko‘rsatkichlarini hisoblashda xatolik yuz berdi',
    LKey.ZH: '计算识别指标时出错',
})
_M_COMET_20_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"COMET-20-QE" هو مقياس لتقييم جودة الترجمة باستخدام نماذج الشبكة العصبية المدربة دون ترجمة مرجعية.',
    LKey.AZ: '"COMET-20-QE" istinad tərcüməsi olmadan təlim keçmiş neyron şəbəkəsi modellərindən istifadə edərək tərcümənin keyfiyyətini qiymətləndirmək üçün bir metrikdir.',
    LKey.DE: '„COMET-20-QE“ ist eine Metrik zur Beurteilung der Übersetzungsqualität mithilfe trainierter neuronaler Netzwerkmodelle ohne Referenzübersetzung.',
    LKey.EN: '"COMET-20-QE" is a metric for assessing the quality of translation using trained neural network models without a reference translation.',
    LKey.ES: '"COMET-20-QE" es una métrica para evaluar la calidad de la traducción utilizando modelos de redes neuronales entrenados sin una traducción de referencia.',
    LKey.FR: "« COMET-20-QE » est une mesure permettant d'évaluer la qualité de la traduction à l'aide de modèles de réseaux neuronaux formés sans traduction de référence.",
    LKey.HI: '"COMET-20-QE" बिना किसी संदर्भ अनुवाद के प्रशिक्षित तंत्रिका नेटवर्क मॉडल का उपयोग करके अनुवाद की गुणवत्ता का आकलन करने के लिए एक मीट्रिक है।',
    LKey.HU: 'A "COMET-20-QE" egy mérőszám a fordítás minőségének értékelésére, betanított neurális hálózati modellek segítségével, referencia fordítás nélkül.',
    LKey.KO: '"COMET-20-QE"는 참조 번역 없이 훈련된 신경망 모델을 사용하여 번역의 품질을 평가하기 위한 지표입니다.',
    LKey.NE: '"COMET-20-QE" कुनै सन्दर्भ अनुवाद बिना प्रशिक्षित न्यूरल नेटवर्क मोडेलहरू प्रयोग गरेर अनुवादको गुणस्तर मूल्याङ्कन गर्ने मेट्रिक हो।',
    LKey.PA: '"COMET-20-QE" ਇੱਕ ਹਵਾਲਾ ਅਨੁਵਾਦ ਦੇ ਬਿਨਾਂ ਸਿਖਲਾਈ ਪ੍ਰਾਪਤ ਨਿਊਰਲ ਨੈਟਵਰਕ ਮਾਡਲਾਂ ਦੀ ਵਰਤੋਂ ਕਰਦੇ ਹੋਏ ਅਨੁਵਾਦ ਦੀ ਗੁਣਵੱਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਨ ਲਈ ਇੱਕ ਮੈਟ੍ਰਿਕ ਹੈ।',
    LKey.RU: '«COMET-20-QE» — метрика для оценки качества перевода с использованием обученных моделей нейронных сетей без эталонного перевода.',
    LKey.TG: '"COMET-20-QE" як ченак барои арзёбии сифати тарҷума бо истифода аз моделҳои омӯзонидашудаи шабакаи нейронӣ бидуни тарҷумаи истинод мебошад.',
    LKey.TL: 'Ang "COMET-20-QE" ay isang sukatan para sa pagtatasa ng kalidad ng pagsasalin gamit ang mga sinanay na modelo ng neural network na walang reference na pagsasalin.',
    LKey.UR: '"COMET-20-QE" بغیر کسی حوالہ ترجمہ کے تربیت یافتہ نیورل نیٹ ورک ماڈلز کا استعمال کرتے ہوئے ترجمے کے معیار کو جانچنے کے لیے ایک میٹرک ہے۔',
    LKey.UZ: '"COMET-20-QE" - mos yozuvlar tarjimasisiz o\'qitilgan neyron tarmoq modellari yordamida tarjima sifatini baholash uchun ko\'rsatkich.',
    LKey.ZH: '“COMET-20-QE”是一种使用经过训练的神经网络模型（无需参考翻译）来评估翻译质量的指标。',
})
_M_COMET_22_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"COMET-22-DA" هو مقياس لتقييم جودة الترجمة باستخدام نماذج الشبكة العصبية المدربة.',
    LKey.AZ: '"COMET-22-DA" təlim keçmiş neyron şəbəkə modellərindən istifadə edərək tərcümənin keyfiyyətini qiymətləndirmək üçün bir metrikdir.',
    LKey.DE: '„COMET-22-DA“ ist eine Metrik zur Beurteilung der Übersetzungsqualität mithilfe trainierter neuronaler Netzwerkmodelle.',
    LKey.EN: '"COMET-22-DA" is a metric for assessing the quality of translation using trained neural network models.',
    LKey.ES: '"COMET-22-DA" es una métrica para evaluar la calidad de la traducción utilizando modelos de redes neuronales entrenados.',
    LKey.FR: "« COMET-22-DA » est une mesure permettant d'évaluer la qualité de la traduction à l'aide de modèles de réseaux neuronaux formés.",
    LKey.HI: '"COMET-22-DA" प्रशिक्षित तंत्रिका नेटवर्क मॉडल का उपयोग करके अनुवाद की गुणवत्ता का आकलन करने के लिए एक मीट्रिक है।',
    LKey.HU: 'A "COMET-22-DA" egy olyan mérőszám, amely a fordítás minőségének felmérésére szolgál, betanított neurális hálózati modellek segítségével.',
    LKey.KO: '"COMET-22-DA"는 훈련된 신경망 모델을 사용하여 번역의 품질을 평가하는 지표입니다.',
    LKey.NE: '"COMET-22-DA" प्रशिक्षित न्यूरल नेटवर्क मोडेलहरू प्रयोग गरेर अनुवादको गुणस्तर मूल्याङ्कन गर्नको लागि मेट्रिक हो।',
    LKey.PA: '"COMET-22-DA" ਸਿਖਲਾਈ ਪ੍ਰਾਪਤ ਨਿਊਰਲ ਨੈਟਵਰਕ ਮਾਡਲਾਂ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਅਨੁਵਾਦ ਦੀ ਗੁਣਵੱਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਨ ਲਈ ਇੱਕ ਮੈਟ੍ਰਿਕ ਹੈ।',
    LKey.RU: '«КОМЕТА-22-ДА» — метрика для оценки качества перевода с использованием обученных моделей нейронных сетей.',
    LKey.TG: '"COMET-22-DA" як метрика барои арзёбии сифати тарҷума бо истифода аз моделҳои омӯзонидашудаи шабакаи нейронӣ мебошад.',
    LKey.TL: 'Ang "COMET-22-DA" ay isang sukatan para sa pagtatasa ng kalidad ng pagsasalin gamit ang mga sinanay na modelo ng neural network.',
    LKey.UR: '"COMET-22-DA" تربیت یافتہ نیورل نیٹ ورک ماڈلز کا استعمال کرتے ہوئے ترجمے کے معیار کو جانچنے کے لیے ایک میٹرک ہے۔',
    LKey.UZ: '"COMET-22-DA" o\'rgatilgan neyron tarmoq modellari yordamida tarjima sifatini baholash uchun ko\'rsatkichdir.',
    LKey.ZH: '“COMET-22-DA”是一种使用训练有素的神经网络模型来评估翻译质量的指标。',
})
_M_BLEU_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"BLEU" هو مقياس لتقييم جودة الترجمة من خلال حساب تطابق مجموعات الكلمات في الترجمة المرجعية.',
    LKey.AZ: '"BLEU" istinad tərcüməsində söz birləşmələrinin üst-üstə düşməsini hesablamaqla tərcümənin keyfiyyətini qiymətləndirmək üçün bir metrikdir.',
    LKey.DE: '„BLEU“ ist eine Metrik zur Beurteilung der Übersetzungsqualität durch Zählen der Übereinstimmung von Wortkombinationen in der Referenzübersetzung.',
    LKey.EN: '"BLEU" is a metric for assessing the quality of translation by counting the coincidence of word combinations in the reference translation.',
    LKey.ES: '"BLEU" es una métrica para evaluar la calidad de la traducción contando la coincidencia de combinaciones de palabras en la traducción de referencia.',
    LKey.FR: "« BLEU » est une mesure permettant d'évaluer la qualité d'une traduction en comptant la coïncidence des combinaisons de mots dans la traduction de référence.",
    LKey.HI: '"BLEU" संदर्भ अनुवाद में शब्द संयोजनों के संयोग की गणना करके अनुवाद की गुणवत्ता का आकलन करने के लिए एक मीट्रिक है।',
    LKey.HU: 'A „BLEU” a fordítás minőségének értékelésére szolgáló mérőszám, amely a referenciafordítás szóösszetételeinek egybeesését számolja.',
    LKey.KO: '"BLEU"는 참조 번역에서 단어 조합의 일치 여부를 계산하여 번역의 품질을 평가하는 지표입니다.',
    LKey.NE: '"BLEU" सन्दर्भ अनुवादमा शब्द संयोजनको संयोग गणना गरेर अनुवादको गुणस्तर मूल्याङ्कन गर्ने मेट्रिक हो।',
    LKey.PA: '"BLEU" ਸੰਦਰਭ ਅਨੁਵਾਦ ਵਿੱਚ ਸ਼ਬਦਾਂ ਦੇ ਸੰਜੋਗਾਂ ਦੇ ਸੰਜੋਗ ਦੀ ਗਿਣਤੀ ਕਰਕੇ ਅਨੁਵਾਦ ਦੀ ਗੁਣਵੱਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਨ ਲਈ ਇੱਕ ਮੈਟ੍ਰਿਕ ਹੈ।',
    LKey.RU: '«BLEU» — метрика оценки качества перевода путем подсчета совпадений словосочетаний в эталонном переводе.',
    LKey.TG: '"BLEU" як ченак барои арзёбии сифати тарҷума тавассути ҳисоб кардани мувофиқати таркиби калимаҳо дар тарҷумаи истинод мебошад.',
    LKey.TL: 'Ang "BLEU" ay isang sukatan para sa pagtatasa ng kalidad ng pagsasalin sa pamamagitan ng pagbibilang ng pagkakataon ng mga kumbinasyon ng salita sa pagsasalin ng sanggunian.',
    LKey.UR: '"BLEU" حوالہ ترجمے میں الفاظ کے مجموعے کے اتفاق کو شمار کرکے ترجمے کے معیار کا اندازہ لگانے کا ایک میٹرک ہے۔',
    LKey.UZ: '"BLEU" - mos yozuvlar tarjimasida so\'z birikmalarining mos kelishini hisoblash orqali tarjima sifatini baholash uchun ko\'rsatkich.',
    LKey.ZH: '“BLEU”是通过计算参考译文中词汇组合的重合程度来评估翻译质量的一种指标。',
})
_M_SONAR_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"SONAR" - مقياس لتقييم جودة الترجمة باستخدام نماذج الشبكة العصبية دون ترجمة مرجعية',
    LKey.AZ: '"SONAR" - istinad tərcüməsi olmadan neyron şəbəkə modellərindən istifadə edərək tərcümənin keyfiyyətini qiymətləndirmək üçün metrik',
    LKey.DE: '„SONAR“ – eine Metrik zur Beurteilung der Übersetzungsqualität mithilfe neuronaler Netzwerkmodelle ohne Referenzübersetzung',
    LKey.EN: '"SONAR" - a metric for assessing the quality of translation using neural network models without a reference translation',
    LKey.ES: '"SONAR": una métrica para evaluar la calidad de la traducción utilizando modelos de redes neuronales sin una traducción de referencia',
    LKey.FR: "« SONAR » - une mesure permettant d'évaluer la qualité de la traduction à l'aide de modèles de réseaux neuronaux sans traduction de référence",
    LKey.HI: '"SONAR" - संदर्भ अनुवाद के बिना तंत्रिका नेटवर्क मॉडल का उपयोग करके अनुवाद की गुणवत्ता का आकलन करने के लिए एक मीट्रिक',
    LKey.HU: '"SONAR" - egy mérőszám a fordítás minőségének értékelésére neurális hálózati modellek segítségével, referencia fordítás nélkül',
    LKey.KO: '"SONAR" - 참조 번역 없이 신경망 모델을 사용하여 번역 품질을 평가하기 위한 지표',
    LKey.NE: '"SONAR" - कुनै सन्दर्भ अनुवाद बिना तंत्रिका नेटवर्क मोडेलहरू प्रयोग गरेर अनुवादको गुणस्तर मूल्याङ्कन गर्नको लागि मेट्रिक',
    LKey.PA: '"SONAR" - ਇੱਕ ਹਵਾਲਾ ਅਨੁਵਾਦ ਦੇ ਬਿਨਾਂ ਨਿਊਰਲ ਨੈਟਵਰਕ ਮਾਡਲਾਂ ਦੀ ਵਰਤੋਂ ਕਰਦੇ ਹੋਏ ਅਨੁਵਾਦ ਦੀ ਗੁਣਵੱਤਾ ਦਾ ਮੁਲਾਂਕਣ ਕਰਨ ਲਈ ਇੱਕ ਮੈਟ੍ਰਿਕ',
    LKey.RU: '«СОНАР» - метрика оценки качества перевода с использованием нейросетевых моделей без эталонного перевода',
    LKey.TG: '"SONAR" - метрика барои арзёбии сифати тарҷума бо истифода аз моделҳои шабакаи нейронӣ бидуни тарҷумаи истинод',
    LKey.TL: '"SONAR" - isang sukatan para sa pagtatasa ng kalidad ng pagsasalin gamit ang mga modelo ng neural network na walang reference na pagsasalin',
    LKey.UR: '"SONAR" - بغیر حوالہ ترجمہ کے نیورل نیٹ ورک ماڈلز کا استعمال کرتے ہوئے ترجمے کے معیار کا اندازہ لگانے کے لیے ایک میٹرک',
    LKey.UZ: '"SONAR" - mos yozuvlar tarjimasisiz neyron tarmoq modellari yordamida tarjima sifatini baholash uchun ko\'rsatkich',
    LKey.ZH: '“SONAR”——一种使用神经网络模型（无需参考翻译）评估翻译质量的指标',
})
_M_CONF_INTERVAL_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"فاصل الثقة للفرق بين المتوسطات" - يتم إنشاؤه باستخدام طريقة الإحصاء التمهيدية. لإنشاء فاصل ثقة صحيح، يجب استيفاء المتطلبات الأساسية التالية:- يجب أن تكون العينة ممثلة (أي يجب تقديم الترجمات لمنتجات/أقسام مختلفة؛ يجب أن تكون الجمل بأطوال مختلفة (قصيرة، متوسطة، طويلة)؛ - يفضل أن يكون حجم الاختبار 300 سطر أو أكثر (مع حجم اختبار صغير، 100 سطر أو أقل، ستكون فاصل الثقة ضيقًا جدًا وقد لا تلتقط القيمة الحقيقية للفرق)',
    LKey.AZ: '"Vasitələrdəki fərqin etibarlılıq intervalı" - bootstrap statistik metodundan istifadə etməklə qurulur. Düzgün etimad intervalı qurmaq üçün aşağıdakı ilkin şərtlər yerinə yetirilməlidir: - nümunə reprezentativ olmalıdır (yəni müxtəlif məhsullar/departamentlər üçün tərcümələr təqdim edilməlidir; cümlələr müxtəlif uzunluqda (qısa, orta, uzun) olmalıdır); - test ölçüsü tercihen 300 sətir və ya daha çox (kiçik test ölçüsü, 100 sətir və ya daha az olduqda, etimad intervalı olduqca dar olacaq və fərqin həqiqi dəyərini tutmaya bilər)',
    LKey.DE: '„Konfidenzintervall der Mittelwertdifferenz“ – wird mithilfe der statistischen Bootstrap-Methode erstellt. Um ein korrektes Konfidenzintervall zu erstellen, müssen die folgenden Voraussetzungen erfüllt sein: – Die Stichprobe muss repräsentativ sein (d. h. Übersetzungen müssen für verschiedene Produkte/Abteilungen vorgelegt werden; Sätze müssen unterschiedliche Längen haben (kurz, mittel, lang); – Die Testgröße beträgt vorzugsweise 300 Zeilen oder mehr (bei einer kleinen Testgröße von 100 Zeilen oder weniger ist das Konfidenzintervall recht eng und erfasst möglicherweise nicht den wahren Wert der Differenz).',
    LKey.EN: '"Confidence interval of the difference in means" - is constructed using the bootstrap statistical method. To construct a correct confidence interval, the following prerequisites must be met:- the sample must be representative (i.e. translations must be presented for different products/departments; sentences must be of different lengths (short, medium, long); - the test size is preferably 300 lines or more (with a small test size, 100 lines or less, the confidence interval will be quite narrow and may not capture the true value of the difference)',
    LKey.ES: 'El intervalo de confianza de la diferencia de medias se construye utilizando el método estadístico bootstrap. Para construir un intervalo de confianza correcto, se deben cumplir los siguientes requisitos previos: - la muestra debe ser representativa (es decir, se deben presentar traducciones para diferentes productos/departamentos; las oraciones deben tener diferentes longitudes (cortas, medianas, largas); - el tamaño de la prueba es preferiblemente de 300 líneas o más (con un tamaño de prueba pequeño, 100 líneas o menos, el intervalo de confianza será bastante estrecho y puede no capturar el valor real de la diferencia)',
    LKey.FR: "« Intervalle de confiance de la différence des moyennes » - est construit en utilisant la méthode statistique bootstrap. Pour construire un intervalle de confiance correct, les conditions préalables suivantes doivent être remplies : - l'échantillon doit être représentatif (c'est-à-dire que les traductions doivent être présentées pour différents produits/départements ; les phrases doivent être de longueurs différentes (courtes, moyennes, longues) ; - la taille du test est de préférence de 300 lignes ou plus (avec une petite taille de test, 100 lignes ou moins, l'intervalle de confiance sera assez étroit et peut ne pas capturer la vraie valeur de la différence)",
    LKey.HI: '"माध्य में अंतर का विश्वास अंतराल" - बूटस्ट्रैप सांख्यिकीय विधि का उपयोग करके बनाया गया है। सही विश्वास अंतराल बनाने के लिए, निम्नलिखित पूर्वापेक्षाएँ पूरी होनी चाहिए: - नमूना प्रतिनिधि होना चाहिए (अर्थात अनुवाद विभिन्न उत्पादों/विभागों के लिए प्रस्तुत किया जाना चाहिए; वाक्य अलग-अलग लंबाई के होने चाहिए (छोटे, मध्यम, लंबे); - परीक्षण का आकार अधिमानतः 300 पंक्तियों या उससे अधिक होना चाहिए (एक छोटे परीक्षण आकार, 100 पंक्तियों या उससे कम के साथ, विश्वास अंतराल काफी संकीर्ण होगा और अंतर के सही मूल्य को नहीं पकड़ सकता है)',
    LKey.HU: '"Az átlagkülönbség konfidencia intervalluma" - a bootstrap statisztikai módszerrel van kialakítva. A megfelelő konfidenciaintervallum felépítéséhez a következő előfeltételeknek kell teljesülniük: - a mintának reprezentatívnak kell lennie (azaz a különböző termékekre/részlegekre vonatkozó fordításokat kell bemutatni; a mondatoknak különböző hosszúságúaknak kell lenniük (rövid, közepes, hosszú); - a teszt mérete lehetőleg 300 sor vagy több (kis tesztmérettel, 100 vagy kevesebb sorral, a konfidenciaintervallum meglehetősen szűk lesz, és előfordulhat, hogy nem rögzíti a különbség valódi értékét)',
    LKey.KO: '"평균 차이의 신뢰 구간"은 부트스트랩 통계적 방법을 사용하여 구성됩니다. 올바른 신뢰 구간을 구성하려면 다음 전제 조건을 충족해야 합니다.- 샘플은 대표적이어야 합니다(즉, 번역은 다른 제품/부서에 대해 제시되어야 함; 문장은 길이가 달라야 함(짧음, 중간, 길음); - 테스트 크기는 300줄 이상이어야 함(테스트 크기가 작으면 100줄 이하일 경우 신뢰 구간이 매우 좁아 차이의 실제 값을 포착하지 못할 수 있음)',
    LKey.NE: '"अर्थमा भिन्नताको आत्मविश्वास अन्तराल" - बुटस्ट्र्याप सांख्यिकीय विधि प्रयोग गरेर निर्माण गरिएको छ। सही विश्वास अन्तराल निर्माण गर्न, निम्न आवश्यकताहरू पूरा गर्नुपर्छ: - नमूना प्रतिनिधि हुनुपर्छ (अर्थात अनुवादहरू विभिन्न उत्पादनहरू/विभागहरूको लागि प्रस्तुत हुनुपर्छ; वाक्यहरू फरक लम्बाइको हुनुपर्छ (छोटो, मध्यम, लामो); - परीक्षण आकार प्राथमिकतामा 300 रेखा वा बढी हो (सानो परीक्षण आकारको साथ, 100 रेखा वा कम, विश्वास अन्तराल एकदम साँघुरो हुनेछ र भिन्नताको वास्तविक मूल्य कब्जा गर्न सक्दैन)',
    LKey.PA: '"ਭਾਵਾਂ ਵਿੱਚ ਅੰਤਰ ਦਾ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ" - ਬੂਟਸਟਰੈਪ ਅੰਕੜਾ ਵਿਧੀ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਬਣਾਇਆ ਗਿਆ ਹੈ। ਇੱਕ ਸਹੀ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ ਬਣਾਉਣ ਲਈ, ਹੇਠ ਲਿਖੀਆਂ ਸ਼ਰਤਾਂ ਪੂਰੀਆਂ ਕੀਤੀਆਂ ਜਾਣੀਆਂ ਚਾਹੀਦੀਆਂ ਹਨ: - ਨਮੂਨਾ ਪ੍ਰਤੀਨਿਧੀ ਹੋਣਾ ਚਾਹੀਦਾ ਹੈ (ਭਾਵ ਅਨੁਵਾਦ ਵੱਖ-ਵੱਖ ਉਤਪਾਦਾਂ/ਵਿਭਾਗਾਂ ਲਈ ਪੇਸ਼ ਕੀਤੇ ਜਾਣੇ ਚਾਹੀਦੇ ਹਨ; ਵਾਕ ਵੱਖ-ਵੱਖ ਲੰਬਾਈ (ਛੋਟੇ, ਦਰਮਿਆਨੇ, ਲੰਬੇ) ਦੇ ਹੋਣੇ ਚਾਹੀਦੇ ਹਨ; - ਟੈਸਟ ਦਾ ਆਕਾਰ ਤਰਜੀਹੀ ਤੌਰ \'ਤੇ 300 ਲਾਈਨਾਂ ਜਾਂ ਵੱਧ ਹਨ (ਛੋਟੇ ਟੈਸਟ ਆਕਾਰ ਦੇ ਨਾਲ, 100 ਲਾਈਨਾਂ ਜਾਂ ਘੱਟ, ਭਰੋਸੇ ਦਾ ਅੰਤਰਾਲ ਕਾਫ਼ੀ ਤੰਗ ਹੋਵੇਗਾ ਅਤੇ ਹੋ ਸਕਦਾ ਹੈ ਕਿ ਅੰਤਰ ਦੇ ਸਹੀ ਮੁੱਲ ਨੂੰ ਹਾਸਲ ਨਾ ਕਰ ਸਕੇ)',
    LKey.RU: '"Доверительный интервал разницы в средних" - строится с использованием статистического метода bootstrap. Для построения правильного доверительного интервала должны быть выполнены следующие предпосылки:- выборка должна быть репрезентативной (т.е. должны быть представлены переводы для разных продуктов/отделов; предложения должны быть разной длины (короткие, средние, длинные); - размер теста предпочтительно 300 строк или более (при небольшом размере теста, 100 строк или менее, доверительный интервал будет довольно узким и может не отражать истинное значение разницы)',
    LKey.TG: '«Фасраи эътимоди тафовут дар воситаҳо» - бо истифода аз усули омори bootstrap сохта шудааст. Барои сохтани фосилаи эътимоди дуруст, шартҳои зерин бояд риоя карда шаванд: - намуна бояд намояндагӣ бошад (яъне тарҷумаҳо барои маҳсулот/шӯъбаҳои гуногун пешниҳод карда шаванд; ҷумлаҳо бояд дарозии гуногун бошанд (кӯтоҳ, миёна, дароз); - андозаи санҷиш. беҳтараш 300 сатр ё бештар аст (бо андозаи хурди санҷиш, 100 сатр ё камтар, фосилаи эътимод хеле танг хоҳад буд ва метавонад арзиши аслии фарқиятро ба даст наорад)',
    LKey.TL: '"Confidence interval of the difference in means" - ay binuo gamit ang bootstrap statistical method. Upang makabuo ng tamang agwat ng kumpiyansa, ang mga sumusunod na kinakailangan ay dapat matugunan:- ang sample ay dapat na kinatawan (ibig sabihin, ang mga pagsasalin ay dapat ipakita para sa iba\'t ibang mga produkto/kagawaran; ang mga pangungusap ay dapat na may iba\'t ibang haba (maikli, katamtaman, mahaba); - ang sukat ng pagsubok mas mainam na 300 linya o higit pa (na may maliit na sukat ng pagsubok, 100 linya o mas kaunti, ang pagitan ng kumpiyansa ay magiging medyo makitid at maaaring hindi makuha ang tunay na halaga ng pagkakaiba)',
    LKey.UR: '"ذرائع میں فرق کا اعتماد کا وقفہ" - بوٹسٹریپ شماریاتی طریقہ استعمال کرتے ہوئے بنایا گیا ہے۔ اعتماد کا صحیح وقفہ بنانے کے لیے، درج ذیل شرائط کو پورا کرنا ضروری ہے: - نمونہ نمائندہ ہونا چاہیے (یعنی مختلف پروڈکٹس/محکموں کے لیے ترجمے پیش کیے جائیں؛ جملے مختلف طوالت کے ہوں (مختصر، درمیانے، طویل)؛ - ٹیسٹ کا سائز ترجیحی طور پر 300 لائنیں یا اس سے زیادہ ہیں (چھوٹے ٹیسٹ سائز کے ساتھ، 100 لائنوں یا اس سے کم، اعتماد کا وقفہ کافی تنگ ہو گا اور فرق کی صحیح قدر کو حاصل نہیں کر سکتا)',
    LKey.UZ: '"O\'rtacha farqning ishonch oralig\'i" - bootstrap statistik usuli yordamida tuziladi. To\'g\'ri ishonch oralig\'ini yaratish uchun quyidagi shartlarga rioya qilish kerak: - namuna reprezentativ bo\'lishi kerak (ya\'ni tarjimalar turli mahsulotlar/bo\'limlar uchun taqdim etilishi kerak; jumlalar turli uzunliklarda bo\'lishi kerak (qisqa, o\'rta, uzun); - test hajmi afzalroq 300 satr yoki undan ko\'p (kichik sinov o\'lchami, 100 satr yoki undan kam bo\'lsa, ishonch oralig\'i juda tor bo\'ladi va farqning haqiqiy qiymatini ushlamasligi mumkin)',
    LKey.ZH: '“均值差异的置信区间”——使用引导统计方法构建。要构建正确的置信区间，必须满足以下先决条件：- 样本必须具有代表性（即必须针对不同的产品/部门提供翻译；句子的长度必须不同（短、中、长）；- 测试规模最好为 300 行或更多（如果测试规模较小，为 100 行或更少，则置信区间将非常狭窄，可能无法捕捉差异的真实值）',
})
_M_ALPHA_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"ALPHA" - مستوى الدلالة؛ ألفا = 0.05 يعني أنه باحتمال 95% فإن القيمة الحقيقية للفرق بين المتوسطات ستكون ضمن فاصل الثقة. واحتمال أن تكون القيمة الحقيقية للفرق بين المتوسطات خارج فاصل الثقة سيكون 5%.',
    LKey.AZ: '"ALPHA" - əhəmiyyət səviyyəsi; alfa = 0.05 o deməkdir ki, 95% ehtimalla vasitələr arasındakı fərqin həqiqi dəyəri etibarlılıq intervalında olacaqdır. Vasitələrdəki fərqin həqiqi dəyərinin inam intervalından kənarda olması ehtimalı 5% olacaqdır.',
    LKey.DE: '„ALPHA“ – Signifikanzniveau; Alpha = 0,05 bedeutet, dass der wahre Wert der Mittelwertdifferenz mit einer Wahrscheinlichkeit von 95 % innerhalb des Konfidenzintervalls liegt. Die Wahrscheinlichkeit, dass der wahre Wert der Mittelwertdifferenz außerhalb des Konfidenzintervalls liegt, beträgt 5 %.',
    LKey.EN: '"ALPHA" - significance level; alpha = 0.05 means that with a probability of 95% the true value of the difference in means will be within the confidence interval. The probability that the true value of the difference in means will be outside the confidence interval will be 5%.',
    LKey.ES: '"ALFA" - nivel de significancia; alfa = 0,05 significa que con una probabilidad del 95% el valor verdadero de la diferencia de medias estará dentro del intervalo de confianza. La probabilidad de que el valor verdadero de la diferencia de medias esté fuera del intervalo de confianza será del 5%.',
    LKey.FR: "« ALPHA » - niveau de signification ; alpha = 0,05 signifie qu'avec une probabilité de 95 %, la valeur réelle de la différence entre les moyennes sera dans l'intervalle de confiance. La probabilité que la valeur réelle de la différence entre les moyennes soit en dehors de l'intervalle de confiance sera de 5 %.",
    LKey.HI: '"अल्फा" - महत्व स्तर; अल्फा = 0.05 का अर्थ है कि 95% की संभावना के साथ माध्य में अंतर का वास्तविक मूल्य विश्वास अंतराल के भीतर होगा। इस बात की संभावना कि माध्य में अंतर का वास्तविक मूल्य विश्वास अंतराल के बाहर होगा, 5% होगी।',
    LKey.HU: '"ALFA" - szignifikancia szint; Az alfa = 0,05 azt jelenti, hogy 95%-os valószínűséggel az átlagok különbségének valódi értéke a konfidencia intervallumon belül lesz. Annak a valószínűsége, hogy az átlagok különbségének valódi értéke kívül esik a konfidenciaintervallumon, 5%.',
    LKey.KO: '"알파" - 유의 수준; 알파 = 0.05는 평균 차이의 참값이 95% 확률로 신뢰 구간 내에 있음을 의미합니다. 평균 차이의 참값이 신뢰 구간 밖에 있을 확률은 5%입니다.',
    LKey.NE: '"अल्फा" - महत्व स्तर; alpha = 0.05 को मतलब 95% को सम्भाव्यता संग मतलब मा भिन्नता को वास्तविक मान विश्वास अन्तराल भित्र हुनेछ। सम्भाव्यता मा भिन्नता को वास्तविक मूल्य विश्वास अन्तराल बाहिर हुनेछ 5% हुनेछ।',
    LKey.PA: '"ਅਲਫਾ" - ਮਹੱਤਤਾ ਦਾ ਪੱਧਰ; alpha = 0.05 ਦਾ ਮਤਲਬ ਹੈ ਕਿ 95% ਦੀ ਸੰਭਾਵਨਾ ਦੇ ਨਾਲ ਮਤਲਬ ਵਿੱਚ ਅੰਤਰ ਦਾ ਅਸਲ ਮੁੱਲ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ ਦੇ ਅੰਦਰ ਹੋਵੇਗਾ। ਸੰਭਾਵਨਾ ਹੈ ਕਿ ਸਾਧਨਾਂ ਵਿੱਚ ਅੰਤਰ ਦਾ ਸਹੀ ਮੁੱਲ ਵਿਸ਼ਵਾਸ ਅੰਤਰਾਲ ਤੋਂ ਬਾਹਰ ਹੋਵੇਗਾ 5%।',
    LKey.RU: '"АЛЬФА" - уровень значимости; альфа = 0,05 означает, что с вероятностью 95% истинное значение разности средних будет находиться в пределах доверительного интервала. Вероятность того, что истинное значение разности средних будет находиться за пределами доверительного интервала, составит 5%.',
    LKey.TG: '"ALPHA" - дараҷаи аҳамият; alpha = 0,05 маънои онро дорад, ки бо эҳтимолияти 95% арзиши ҳақиқии фарқият дар воситаҳо дар фосилаи эътимод хоҳад буд. Эҳтимолияти берун аз фосилаи эътимод будани арзиши ҳақиқии фарқият 5% хоҳад буд.',
    LKey.TL: '"ALPHA" - antas ng kahalagahan; alpha = 0.05 ay nangangahulugan na may probabilidad na 95% ang tunay na halaga ng pagkakaiba sa ibig sabihin ay nasa loob ng confidence interval. Ang posibilidad na ang tunay na halaga ng pagkakaiba sa mga paraan ay nasa labas ng pagitan ng kumpiyansa ay magiging 5%.',
    LKey.UR: '"الفا" - اہمیت کی سطح؛ alpha = 0.05 کا مطلب ہے کہ 95% کے امکان کے ساتھ ذرائع میں فرق کی حقیقی قدر اعتماد کے وقفے کے اندر ہوگی۔ اس بات کا امکان کہ ذرائع میں فرق کی حقیقی قدر اعتماد کے وقفے سے باہر ہو گی 5%۔',
    LKey.UZ: '"ALPHA" - ahamiyatlilik darajasi; alfa = 0,05, 95% ehtimollik bilan vositalardagi farqning haqiqiy qiymati ishonch oralig\'ida bo\'lishini anglatadi. O\'rtacha farqning haqiqiy qiymati ishonch oralig\'idan tashqarida bo\'lish ehtimoli 5% ni tashkil qiladi.',
    LKey.ZH: '“ALPHA” - 重要性水平；alpha = 0.05 表示均值差的真实值在置信区间内的概率为 95%。均值差的真实值在置信区间之外的概率为 5%。',
})
_M_P_VAL_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"القيمة الاحتمالية" - احتمال أن يكون الفرق بين المتوسطات صفرًا؛ مقارنة بمستوى الدلالة ألفا. إذا كانت القيمة الاحتمالية أكبر من أو تساوي ألفا، فهذا يعني أنه ليس لدينا سبب لرفض الفرضية الصفرية (جودة الترجمة للنظامين متكافئة). إذا كانت القيمة الاحتمالية أقل من ألفا، يتم رفض الفرضية الصفرية (جودة النظامين مختلفة).',
    LKey.AZ: '"P-VALUE" - vasitələr arasındakı fərqin sıfır olacağı ehtimalı; əhəmiyyət səviyyəsi alfa ilə müqayisədə. Əgər p-dəyəri alfa-dan böyük və ya bərabərdirsə, bu o deməkdir ki, bizim sıfır fərziyyəni rədd etmək üçün heç bir səbəbimiz yoxdur (iki sistemin tərcümə keyfiyyəti ekvivalentdir). Əgər p-dəyəri alfadan azdırsa, sıfır hipotezi rədd edilir (iki sistemin keyfiyyəti fərqlidir).',
    LKey.DE: '„P-WERT“ – die Wahrscheinlichkeit, dass die Differenz zwischen den Mittelwerten Null ergibt; verglichen mit dem Signifikanzniveau Alpha. Wenn der P-Wert größer oder gleich Alpha ist, bedeutet dies, dass wir keinen Grund haben, die Nullhypothese abzulehnen (die Übersetzungsqualität der beiden Systeme ist gleichwertig). Wenn der P-Wert kleiner als Alpha ist, wird die Nullhypothese abgelehnt (die Qualität der beiden Systeme ist unterschiedlich).',
    LKey.EN: '"P-VALUE" - the probability that the difference between the means will be zero; compared with the significance level alpha. If the p-value is greater than or equal to alpha, this means that we have no reason to reject the null hypothesis (the translation quality of the two systems is equivalent). If the p-value is less than alpha, the null hypothesis is rejected (the quality of the two systems differs).',
    LKey.ES: '"P-VALUE" - la probabilidad de que la diferencia entre las medias sea cero; comparada con el nivel de significación alfa. Si el p-valor es mayor o igual a alfa, esto significa que no tenemos ninguna razón para rechazar la hipótesis nula (la calidad de la traducción de los dos sistemas es equivalente). Si el p-valor es menor que alfa, la hipótesis nula se rechaza (la calidad de los dos sistemas difiere).',
    LKey.FR: "« P-VALUE » - la probabilité que la différence entre les moyennes soit nulle ; comparée au niveau de signification alpha. Si la p-value est supérieure ou égale à alpha, cela signifie que nous n'avons aucune raison de rejeter l'hypothèse nulle (la qualité de traduction des deux systèmes est équivalente). Si la p-value est inférieure à alpha, l'hypothèse nulle est rejetée (la qualité des deux systèmes diffère).",
    LKey.HI: '"पी-वैल्यू" - संभावना है कि माध्य के बीच का अंतर शून्य होगा; महत्व स्तर अल्फा के साथ तुलना में। यदि पी-वैल्यू अल्फा से अधिक या बराबर है, तो इसका मतलब है कि हमारे पास शून्य परिकल्पना को अस्वीकार करने का कोई कारण नहीं है (दोनों प्रणालियों की अनुवाद गुणवत्ता बराबर है)। यदि पी-वैल्यू अल्फा से कम है, तो शून्य परिकल्पना को अस्वीकार कर दिया जाता है (दोनों प्रणालियों की गुणवत्ता अलग-अलग होती है)।',
    LKey.HU: '"P-ÉRTÉK" - annak valószínűsége, hogy az átlagok közötti különbség nulla lesz; az alfa szignifikanciaszinthez képest. Ha a p-érték nagyobb vagy egyenlő, mint alfa, ez azt jelenti, hogy nincs okunk a nullhipotézis elutasítására (a két rendszer fordítási minősége egyenértékű). Ha a p-érték kisebb, mint az alfa, akkor a nullhipotézist elvetjük (a két rendszer minősége eltér).',
    LKey.KO: '"P-값" - 평균 차이가 0이 될 확률; 유의 수준 알파와 비교. p-값이 알파보다 크거나 같으면 귀무 가설을 기각할 이유가 없음을 의미합니다(두 시스템의 변환 품질이 동일함). p-값이 알파보다 작으면 귀무 가설이 기각됩니다(두 시스템의 품질이 다름).',
    LKey.NE: '"P-VALUE" - साधनहरू बीचको भिन्नता शून्य हुने सम्भावना; महत्व स्तर अल्फा संग तुलना। यदि p-मान अल्फा भन्दा ठूलो वा बराबर छ भने, यसको मतलब हामीसँग शून्य परिकल्पना अस्वीकार गर्ने कुनै कारण छैन (दुई प्रणालीहरूको अनुवाद गुणस्तर बराबर छ)। यदि p-मान अल्फा भन्दा कम छ भने, शून्य परिकल्पना अस्वीकार गरिएको छ (दुई प्रणालीहरूको गुणस्तर फरक छ)।',
    LKey.PA: '"P-VALUE" - ਸੰਭਾਵਨਾ ਹੈ ਕਿ ਸਾਧਨਾਂ ਵਿਚਕਾਰ ਅੰਤਰ ਜ਼ੀਰੋ ਹੋਵੇਗਾ; ਮਹੱਤਵ ਪੱਧਰ ਐਲਫ਼ਾ ਨਾਲ ਤੁਲਨਾ ਕੀਤੀ ਗਈ। ਜੇਕਰ p-ਮੁੱਲ ਅਲਫ਼ਾ ਤੋਂ ਵੱਧ ਜਾਂ ਬਰਾਬਰ ਹੈ, ਤਾਂ ਇਸਦਾ ਮਤਲਬ ਹੈ ਕਿ ਸਾਡੇ ਕੋਲ ਨਲ ਪਰਿਕਲਪਨਾ ਨੂੰ ਰੱਦ ਕਰਨ ਦਾ ਕੋਈ ਕਾਰਨ ਨਹੀਂ ਹੈ (ਦੋਵਾਂ ਪ੍ਰਣਾਲੀਆਂ ਦੀ ਅਨੁਵਾਦ ਗੁਣਵੱਤਾ ਬਰਾਬਰ ਹੈ)। ਜੇਕਰ p-ਮੁੱਲ ਅਲਫ਼ਾ ਤੋਂ ਘੱਟ ਹੈ, ਤਾਂ ਨਲ ਪਰਿਕਲਪਨਾ ਨੂੰ ਰੱਦ ਕਰ ਦਿੱਤਾ ਜਾਂਦਾ ਹੈ (ਦੋਵਾਂ ਪ੍ਰਣਾਲੀਆਂ ਦੀ ਗੁਣਵੱਤਾ ਵੱਖਰੀ ਹੁੰਦੀ ਹੈ)।',
    LKey.RU: '"P-ЗНАЧЕНИЕ" - вероятность того, что разница между средними будет равна нулю; по сравнению с уровнем значимости альфа. Если p-значение больше или равно альфа, это означает, что у нас нет причин отвергать нулевую гипотезу (качество перевода двух систем эквивалентно). Если p-значение меньше альфа, нулевая гипотеза отвергается (качество двух систем различается).',
    LKey.TG: '"P-VALUE" - эҳтимолияти ба сифр баробар шудани фарқияти байни миёнаравҳо; дар муқоиса бо сатҳи аҳамияти алфа. Агар арзиши p аз алфа бузургтар ё баробар бошад, ин маънои онро дорад, ки мо барои рад кардани фарзияи нол сабабе надорем (сифати тарҷумаи ду система ба ҳам баробар аст). Агар арзиши p-аз алфа камтар бошад, гипотезаи нул рад карда мешавад (сифати ду система фарқ мекунад).',
    LKey.TL: '"P-VALUE" - ang posibilidad na ang pagkakaiba sa pagitan ng mga ibig sabihin ay magiging zero; kumpara sa antas ng kabuluhan na alpha. Kung ang p-value ay mas malaki kaysa o katumbas ng alpha, nangangahulugan ito na wala tayong dahilan upang tanggihan ang null hypothesis (ang kalidad ng pagsasalin ng dalawang sistema ay katumbas). Kung ang p-value ay mas mababa sa alpha, ang null hypothesis ay tinatanggihan (ang kalidad ng dalawang sistema ay naiiba).',
    LKey.UR: '"P-VALUE" - اس بات کا امکان کہ ذرائع کے درمیان فرق صفر ہو جائے گا۔ اہمیت کی سطح الفا کے مقابلے میں۔ اگر p-value الفا سے زیادہ یا اس کے برابر ہے، تو اس کا مطلب ہے کہ ہمارے پاس null hypothesis کو مسترد کرنے کی کوئی وجہ نہیں ہے (دونوں نظاموں کا ترجمہ معیار مساوی ہے)۔ اگر p-value الفا سے کم ہے تو، null hypothesis کو مسترد کر دیا جاتا ہے (دونوں نظاموں کا معیار مختلف ہے)۔',
    LKey.UZ: '"P-VALUE" - vositalar orasidagi farq nolga teng bo\'lish ehtimoli; muhimlik darajasi alfa bilan solishtirganda. Agar p-qiymati alfa dan katta yoki teng bo\'lsa, bu bizda nol gipotezani rad etish uchun hech qanday sabab yo\'qligini anglatadi (ikki tizimning tarjima sifati ekvivalent). Agar p-qiymati alfadan kichik bo\'lsa, nol gipoteza rad etiladi (ikki tizimning sifati farqlanadi).',
    LKey.ZH: '“P 值” - 与显著性水平 alpha 相比，均值之间的差异为零的概率。如果 p 值大于或等于 alpha，则意味着我们没有理由拒绝零假设（两个系统的翻译质量相同）。如果 p 值小于 alpha，则拒绝零假设（两个系统的质量不同）。',
})
_M_STD_DEV_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"الانحراف المعياري" - يوضح مدى انتشار القيم في البيانات بالنسبة لمتوسطها.',
    LKey.AZ: '"Standart sapma" - verilənlərdəki dəyərlərin ortalarına nisbətən nə qədər geniş səpələndiyini göstərir.',
    LKey.DE: '„Standardabweichung“ – zeigt, wie weit die Werte in den Daten im Verhältnis zu ihrem Mittelwert streuen.',
    LKey.EN: '"Standard Deviation" - shows how widely the values in the data are scattered relative to their mean.',
    LKey.ES: '"Desviación estándar": muestra qué tan ampliamente están dispersos los valores de los datos en relación con su media.',
    LKey.FR: '« Écart type » : montre dans quelle mesure les valeurs des données sont dispersées par rapport à leur moyenne.',
    LKey.HI: '"मानक विचलन" - यह दर्शाता है कि डेटा में मान अपने माध्य के सापेक्ष कितने व्यापक रूप से बिखरे हुए हैं।',
    LKey.HU: '"Standard Deviation" - megmutatja, hogy az adatokban szereplő értékek milyen széles körben szóródnak az átlagukhoz képest.',
    LKey.KO: '"표준편차" - 데이터의 값이 평균에 비해 얼마나 넓게 퍼져 있는지를 보여줍니다.',
    LKey.NE: '"मानक विचलन" - डेटामा मानहरू तिनीहरूको औसतको सापेक्ष कत्तिको व्यापक रूपमा फैलिएको छ भनेर देखाउँछ।',
    LKey.PA: '"ਸਟੈਂਡਰਡ ਡਿਵੀਏਸ਼ਨ" - ਦਿਖਾਉਂਦਾ ਹੈ ਕਿ ਡੇਟਾ ਵਿੱਚ ਮੁੱਲ ਉਹਨਾਂ ਦੇ ਮੱਧਮਾਨ ਦੇ ਅਨੁਸਾਰ ਕਿੰਨੇ ਵਿਆਪਕ ਤੌਰ \'ਤੇ ਖਿੰਡੇ ਹੋਏ ਹਨ।',
    LKey.RU: '«Стандартное отклонение» — показывает, насколько широко разбросаны значения в данных относительно их среднего значения.',
    LKey.TG: '"Интихоби стандартӣ" - нишон медиҳад, ки то чӣ андоза арзишҳо дар додаҳо нисбат ба миёнаи онҳо паҳн шудаанд.',
    LKey.TL: '"Standard Deviation" - ipinapakita kung gaano kalawak ang mga halaga sa data ay nakakalat kaugnay sa kanilang mean.',
    LKey.UR: '"معیاری انحراف" - ظاہر کرتا ہے کہ ڈیٹا میں قدریں ان کے اوسط کے مقابلے میں کتنی وسیع پیمانے پر بکھری ہوئی ہیں۔',
    LKey.UZ: '"Standart og\'ish" - ma\'lumotlardagi qiymatlarning o\'rtachaga nisbatan qanchalik keng tarqalganligini ko\'rsatadi.',
    LKey.ZH: '“标准差”——显示数据中的值相对于其平均值的分散程度。',
})
_M_MEDIAN_DESC_MAP: Final = FrozenDict({
    LKey.AR: 'الوسيط هو مقياس يقسم مجموعة من البيانات إلى نصفين متساويين. نصف البيانات أقل من الوسيط، ونصف البيانات أكبر من الوسيط.',
    LKey.AZ: 'Median bir çox məlumatı iki bərabər yarıya bölən ölçüdür. Verilənlərin yarısı mediandan azdır, məlumatların yarısı isə mediandan böyükdür.',
    LKey.DE: 'Der Median ist ein Maß, das einen Datensatz in zwei gleiche Hälften teilt. Die Hälfte der Daten ist kleiner als der Median, die andere Hälfte größer als der Median.',
    LKey.EN: 'Median is a measure that divides a set of data into two equal halves. Half of the data is less than the median, and half of the data is greater than the median.',
    LKey.ES: 'La mediana es una medida que divide un conjunto de datos en dos mitades iguales. La mitad de los datos es menor que la mediana y la otra mitad es mayor que la mediana.',
    LKey.FR: "La médiane est une mesure qui divise un ensemble de données en deux moitiés égales. La moitié des données est inférieure à la médiane et l'autre moitié est supérieure à la médiane.",
    LKey.HI: 'माध्यिका एक माप है जो डेटा के एक सेट को दो बराबर हिस्सों में विभाजित करता है। डेटा का आधा हिस्सा माध्यिका से कम होता है, और डेटा का आधा हिस्सा माध्यिका से अधिक होता है।',
    LKey.HU: 'A medián egy olyan mérték, amely egy adathalmazt két egyenlő részre oszt. Az adatok fele kisebb a mediánnál, az adatok fele nagyobb, mint a medián.',
    LKey.KO: '중앙값은 데이터 집합을 두 개의 동일한 절반으로 나누는 측정값입니다. 데이터의 절반은 중앙값보다 작고, 데이터의 절반은 중앙값보다 큽니다.',
    LKey.NE: 'माध्य एक मापन हो जसले डेटाको सेटलाई दुई बराबर भागहरूमा विभाजन गर्दछ। आधा डाटा माध्य भन्दा कम छ, र डाटा को आधा माध्य भन्दा ठूलो छ।',
    LKey.PA: 'ਮੱਧਮਾਨ ਇੱਕ ਮਾਪ ਹੈ ਜੋ ਡੇਟਾ ਦੇ ਇੱਕ ਸਮੂਹ ਨੂੰ ਦੋ ਬਰਾਬਰ ਹਿੱਸਿਆਂ ਵਿੱਚ ਵੰਡਦਾ ਹੈ। ਅੱਧਾ ਡੇਟਾ ਮੱਧਮਾਨ ਤੋਂ ਘੱਟ ਹੈ, ਅਤੇ ਅੱਧਾ ਡੇਟਾ ਮੱਧਮਾਨ ਤੋਂ ਵੱਡਾ ਹੈ।',
    LKey.RU: 'Медиана — это мера, которая делит набор данных на две равные половины. Половина данных меньше медианы, а половина данных больше медианы.',
    LKey.TG: 'Медиан ченакест, ки маҷмӯи маълумотро ба ду нисфи баробар тақсим мекунад. Нисфи маълумот аз медиана камтар аст ва нисфи маълумот аз медиана зиёдтар аст.',
    LKey.TL: 'Ang Median ay isang sukatan na naghahati sa isang set ng data sa dalawang pantay na kalahati. Ang kalahati ng data ay mas mababa sa median, at kalahati ng data ay mas malaki kaysa sa median.',
    LKey.UR: 'میڈین ایک ایسا پیمانہ ہے جو ڈیٹا کے سیٹ کو دو برابر حصوں میں تقسیم کرتا ہے۔ آدھا ڈیٹا میڈین سے کم ہے، اور آدھا ڈیٹا میڈین سے بڑا ہے۔',
    LKey.UZ: "Median - ma'lumotlar to'plamini ikkita teng yarmiga bo'ladigan o'lchov. Ma'lumotlarning yarmi medianadan kichikroq va ma'lumotlarning yarmi medianadan kattaroqdir.",
    LKey.ZH: '中位数是将一组数据分成相等的两半的度量。一半数据小于中位数，另一半数据大于中位数。',
})
_M_IQR_DESC_MAP: Final = FrozenDict({
    LKey.AR: '"IQR" (المدى الربعي) - يوضح النطاق الذي يقع فيه 50% من البيانات.',
    LKey.AZ: '"IQR" (interquartile Range) - məlumatların 50% -nin yerləşdiyi diapazonu göstərir.',
    LKey.DE: '„IQR“ (Interquartilbereich) – zeigt den Bereich, in dem 50 % der Daten liegen.',
    LKey.EN: '"IQR" (Interquartile Range) - shows the range in which 50% of the data lies.',
    LKey.ES: '"RIC" (rango intercuartil): muestra el rango en el que se encuentra el 50% de los datos.',
    LKey.FR: '« IQR » (Interquartile Range) - indique la plage dans laquelle se trouvent 50 % des données.',
    LKey.HI: '"आईक्यूआर" (इंटरक्वार्टाइल रेंज) - वह रेंज दिखाता है जिसमें 50% डेटा निहित होता है।',
    LKey.HU: '"IQR" (interkvartilis tartomány) - azt a tartományt mutatja, amelyben az adatok 50%-a található.',
    LKey.KO: '"IQR"(사분위 범위) - 데이터의 50%가 속하는 범위를 보여줍니다.',
    LKey.NE: '"IQR" (Interquartile दायरा) - दायरा देखाउँछ जसमा 50% डाटा निहित छ।',
    LKey.PA: '"IQR" (ਇੰਟਰਕੁਆਰਟਾਈਲ ਰੇਂਜ) - ਉਹ ਰੇਂਜ ਦਿਖਾਉਂਦਾ ਹੈ ਜਿਸ ਵਿੱਚ 50% ਡੇਟਾ ਹੁੰਦਾ ਹੈ।',
    LKey.RU: '«IQR» (межквартильный размах) — показывает диапазон, в котором находится 50% данных.',
    LKey.TG: '"IQR" (Interquartile Range) - диапазонеро нишон медиҳад, ки дар он 50% маълумот ҷойгир аст.',
    LKey.TL: '"IQR" (Interquartile Range) - ipinapakita ang hanay kung saan namamalagi ang 50% ng data.',
    LKey.UR: '"IQR" (Interquartile Range) - وہ رینج دکھاتا ہے جس میں 50% ڈیٹا ہوتا ہے۔',
    LKey.UZ: '"IQR" (Interquartile Range) - ma\'lumotlarning 50% ni tashkil etadigan diapazonni ko\'rsatadi.',
    LKey.ZH: '“IQR”（四分位距）——显示 50% 数据所在的范围。',
})

_A_MESSAGE_TYPE_MAP: Final = FrozenDict({
    LKey.AR: 'نوع الرسالة',
    LKey.AZ: 'Mesaj növü',
    LKey.DE: 'Nachrichtentyp',
    LKey.EN: 'Message type',
    LKey.ES: 'Tipo de mensaje',
    LKey.FR: 'Type de message',
    LKey.HI: 'संदेश का प्रकार',
    LKey.HU: 'Üzenet típusa',
    LKey.KO: '메시지 유형',
    LKey.NE: 'सन्देश प्रकार',
    LKey.PA: 'ਸੁਨੇਹਾ ਕਿਸਮ',
    LKey.RU: 'Тип сообщения',
    LKey.TG: 'Навъи паём',
    LKey.TL: 'Uri ng mensahe',
    LKey.UR: 'پیغام کی قسم',
    LKey.UZ: 'Xabar turi',
    LKey.ZH: '消息类型',
})
_A_MESSAGE_START_MAP: Final = FrozenDict({
    LKey.AR: 'الرسالة تبدأ في',
    LKey.AZ: 'Mesaj başlayır',
    LKey.DE: 'Nachrichtenbeginn',
    LKey.EN: 'Message start at',
    LKey.ES: 'El mensaje comienza en',
    LKey.FR: 'Le message commence à',
    LKey.HI: 'संदेश प्रारंभ',
    LKey.HU: 'Az üzenet kezdete:',
    LKey.KO: '메시지 시작',
    LKey.NE: 'सन्देश सुरु हुन्छ',
    LKey.PA: 'ਸੁਨੇਹਾ ਸ਼ੁਰੂ ਹੁੰਦਾ ਹੈ',
    LKey.RU: 'Начало сообщения',
    LKey.TG: 'Паём оғоз мешавад',
    LKey.TL: 'Magsisimula ang mensahe sa',
    LKey.UR: 'پیغام شروع ہوتا ہے۔',
    LKey.UZ: 'Xabarning boshlanishi:',
    LKey.ZH: '消息开始于',
})
_A_TARGET_LANGUAGE_MAP: Final = FrozenDict({
    LKey.AR: 'اللغة المستهدفة',
    LKey.AZ: 'Hədəf dili',
    LKey.DE: 'Zielsprache',
    LKey.EN: 'Target language',
    LKey.ES: 'Lengua de llegada',
    LKey.FR: 'Langue cible',
    LKey.HI: 'लक्ष्य भाषा',
    LKey.HU: 'Célnyelv',
    LKey.KO: '대상 언어',
    LKey.NE: 'लक्षित भाषा',
    LKey.PA: 'ਨਿਸ਼ਾਨਾ ਭਾਸ਼ਾ',
    LKey.RU: 'Целевой язык',
    LKey.TG: 'Забони мақсаднок',
    LKey.TL: 'Target na wika',
    LKey.UR: 'ہدف کی زبان',
    LKey.UZ: 'Maqsadli til',
    LKey.ZH: '目标语言',
})
_A_EDITING_TIME_MAP: Final = FrozenDict({
    LKey.AR: 'وقت التحرير',
    LKey.AZ: 'Redaktə vaxtı',
    LKey.DE: 'Bearbeitungszeit',
    LKey.EN: 'Editing time',
    LKey.ES: 'Tiempo de edición',
    LKey.FR: 'Temps de montage',
    LKey.HI: 'संपादन समय',
    LKey.HU: 'Szerkesztési idő',
    LKey.KO: '편집 시간',
    LKey.NE: 'सम्पादन समय',
    LKey.PA: 'ਸੰਪਾਦਨ ਕਰਨ ਦਾ ਸਮਾਂ',
    LKey.RU: 'Время редактирования',
    LKey.TG: 'Вақти таҳрир',
    LKey.TL: 'Oras ng pag-edit',
    LKey.UR: 'ترمیم کا وقت',
    LKey.UZ: 'Tahrirlash vaqti',
    LKey.ZH: '编辑时间',
})
_A_OPERATOR_NAME_MAP: Final = FrozenDict({
    LKey.AR: 'اسم المشغل',
    LKey.AZ: 'Operator adı',
    LKey.DE: 'Name des Betreibers',
    LKey.EN: 'Operator name',
    LKey.ES: 'Nombre del operador',
    LKey.FR: "Nom de l'opérateur",
    LKey.HI: 'ऑपरेटर का नाम',
    LKey.HU: 'Üzemeltető neve',
    LKey.KO: '운영자 이름',
    LKey.NE: 'अपरेटरको नाम',
    LKey.PA: 'ਆਪਰੇਟਰ ਦਾ ਨਾਮ',
    LKey.RU: 'Имя оператора',
    LKey.TG: 'Номи оператор',
    LKey.TL: 'Pangalan ng operator',
    LKey.UR: 'آپریٹر کا نام',
    LKey.UZ: 'Operator nomi',
    LKey.ZH: '运营商名称',
})
_A_AUDIO_UUID_MAP: Final = FrozenDict({
    LKey.AR: 'معرف الصوت العالمي',
    LKey.AZ: 'Audio UUID',
    LKey.DE: 'Audio-UUID',
    LKey.EN: 'Audio UUID',
    LKey.ES: 'UUID de audio',
    LKey.FR: 'UUID audio',
    LKey.HI: 'ऑडियो UUID',
    LKey.HU: 'Audio UUID',
    LKey.KO: '오디오 UUID',
    LKey.NE: 'अडियो UUID',
    LKey.PA: 'ਆਡੀਓ UUID',
    LKey.RU: 'Аудио UUID',
    LKey.TG: 'Audio UUID',
    LKey.TL: 'Audio UUID',
    LKey.UR: 'آڈیو UUID',
    LKey.UZ: 'Audio UUID',
    LKey.ZH: '音频 UUID',
})

_A_CONFIRM_DELETE_CONV_MAP: Final = FrozenDict({
    LKey.AR: 'هل أنت متأكد أنك تريد حذف هذا الحوار؟',
    LKey.AZ: 'Bu dialoqu silmək istədiyinizə əminsiniz?',
    LKey.DE: 'Möchten Sie diesen Dialog wirklich löschen?',
    LKey.EN: 'Are you sure you want to delete this dialog?',
    LKey.ES: '¿Está seguro de que desea eliminar este cuadro de diálogo?',
    LKey.FR: 'Etes-vous sûr de vouloir supprimer cette boîte de dialogue?',
    LKey.HI: 'क्या आप वाकई इस संवाद को हटाना चाहते हैं?',
    LKey.HU: 'Biztosan törli ezt a párbeszédpanelt?',
    LKey.KO: '이 대화 상자를 삭제하시겠습니까?',
    LKey.NE: 'के तपाइँ यो संवाद मेटाउन निश्चित हुनुहुन्छ?',
    LKey.PA: 'ਕੀ ਤੁਸੀਂ ਯਕੀਨਨ ਇਸ ਡਾਇਲਾਗ ਨੂੰ ਮਿਟਾਉਣਾ ਚਾਹੁੰਦੇ ਹੋ?',
    LKey.RU: 'Вы уверены, что хотите удалить этот диалог?',
    LKey.TG: 'Шумо мутмаин ҳастед, ки мехоҳед ин муколамаро нест кунед?',
    LKey.TL: 'Sigurado ka bang gusto mong tanggalin ang dialog na ito?',
    LKey.UR: 'کیا آپ واقعی اس ڈائیلاگ کو حذف کرنا چاہتے ہیں؟',
    LKey.UZ: 'Haqiqatan ham bu dialog oynasini oʻchirib tashlamoqchimisiz?',
    LKey.ZH: '您确实要删除该对话框吗？',
})
_A_USER_DEL_HIMSELF_MAP: Final = FrozenDict({
    LKey.AR: 'لا يمكن للمستخدم حذف نفسه.',
    LKey.AZ: 'İstifadəçi özünü silə bilməz.',
    LKey.DE: 'Der Benutzer kann sich nicht selbst löschen.',
    LKey.EN: 'The user cannot delete himself.',
    LKey.ES: 'El usuario no puede eliminarse a sí mismo.',
    LKey.FR: "L'utilisateur ne peut pas se supprimer lui-même.",
    LKey.HI: 'उपयोगकर्ता स्वयं को हटा नहीं सकता।',
    LKey.HU: 'A felhasználó nem törölheti magát.',
    LKey.KO: '사용자는 자신을 삭제할 수 없습니다.',
    LKey.NE: 'प्रयोगकर्ताले आफूलाई मेटाउन सक्दैन।',
    LKey.PA: 'ਉਪਭੋਗਤਾ ਆਪਣੇ ਆਪ ਨੂੰ ਮਿਟਾ ਨਹੀਂ ਸਕਦਾ।',
    LKey.RU: 'Пользователь не может удалить себя сам.',
    LKey.TG: 'Истифодабаранда наметавонад худро нест кунад.',
    LKey.TL: 'Hindi matanggal ng user ang kanyang sarili.',
    LKey.UR: 'صارف خود کو حذف نہیں کر سکتا۔',
    LKey.UZ: "Foydalanuvchi o'zini o'chira olmaydi.",
    LKey.ZH: '用户不能删除自己。',
})
_A_DIALOGS_COUNT_MAP: Final = FrozenDict({
    LKey.AR: 'عدد الحوارات:',
    LKey.AZ: 'Dialoqların sayı:',
    LKey.DE: 'Anzahl der Dialoge:',
    LKey.EN: 'Dialogs count:',
    LKey.ES: 'Los diálogos cuentan:',
    LKey.FR: 'Les dialogues comptent :',
    LKey.HI: 'संवादों की संख्या:',
    LKey.HU: 'Párbeszédek száma:',
    LKey.KO: '대화의 수:',
    LKey.NE: 'संवाद गणना:',
    LKey.PA: 'ਸੰਵਾਦਾਂ ਦੀ ਗਿਣਤੀ:',
    LKey.RU: 'Количество диалогов:',
    LKey.TG: 'Шумораи диалогҳо:',
    LKey.TL: 'Bilang ng mga dialog:',
    LKey.UR: 'ڈائیلاگ گنتی:',
    LKey.UZ: 'Dialoglar soni:',
    LKey.ZH: '对话计数：',
})
_A_BASE_ERROR_DELETE_USER_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ أثناء حذف المستخدم',
    LKey.AZ: 'İstifadəçini silərkən xəta baş verdi',
    LKey.DE: 'Fehler beim Löschen des Benutzers',
    LKey.EN: 'Error while deleting user',
    LKey.ES: 'Error al eliminar usuario',
    LKey.FR: "Erreur lors de la suppression de l'utilisateur",
    LKey.HI: 'उपयोगकर्ता हटाते समय त्रुटि',
    LKey.HU: 'Hiba történt a felhasználó törlése közben',
    LKey.KO: '사용자 삭제 중 오류 발생',
    LKey.NE: 'प्रयोगकर्ता मेट्दा त्रुटि',
    LKey.PA: 'ਉਪਭੋਗਤਾ ਨੂੰ ਮਿਟਾਉਣ ਦੌਰਾਨ ਗਲਤੀ',
    LKey.RU: 'Ошибка при удалении пользователя',
    LKey.TG: 'Хатогӣ ҳангоми нест кардани корбар',
    LKey.TL: 'Error habang tinatanggal ang user',
    LKey.UR: 'صارف کو حذف کرتے وقت خرابی',
    LKey.UZ: 'Foydalanuvchini oʻchirishda xatolik yuz berdi',
    LKey.ZH: '删除用户时出错',
})
_A_ERROR_DELETE_CONV_MAP: Final = FrozenDict({
    LKey.AR: 'خطأ أثناء حذف الحوار',
    LKey.AZ: 'Dialoqu silərkən xəta baş verdi',
    LKey.DE: 'Fehler beim Löschen des Dialogs',
    LKey.EN: 'Error while deleting dialog',
    LKey.ES: 'Error al eliminar el diálogo',
    LKey.FR: 'Erreur lors de la suppression de la boîte de dialogue',
    LKey.HI: 'संवाद हटाते समय त्रुटि हुई',
    LKey.HU: 'Hiba történt a párbeszédpanel törlése közben',
    LKey.KO: '대화 상자 삭제 중 오류 발생',
    LKey.NE: 'संवाद मेटाउँदा त्रुटि भयो',
    LKey.PA: 'ਡਾਇਲਾਗ ਮਿਟਾਉਣ ਦੌਰਾਨ ਗਲਤੀ',
    LKey.RU: 'Ошибка при удалении диалога',
    LKey.TG: 'Хатогӣ ҳангоми нест кардани муколама',
    LKey.TL: 'Error habang tinatanggal ang dialog',
    LKey.UR: 'ڈائیلاگ کو حذف کرتے وقت خرابی',
    LKey.UZ: 'Muloqot oynasini oʻchirishda xatolik yuz berdi',
    LKey.ZH: '删除对话框时出错',
})

#####################################################################################################
# AUTOGENERATE_END
#####################################################################################################

_NOTRANSLATE_WRAP_PATTERN: Final = _re_compile(r'(\[@(?P<non_translated>.*?)@\])', MULTILINE | UNICODE)

#####################################################################################################

def _get_notranslate_group(match: Match[str]) -> str:
    return match.group('non_translated')

#####################################################################################################

def _clean_notranslate_wraps(text: str) -> str:
    return _NOTRANSLATE_WRAP_PATTERN.sub(_get_notranslate_group, text)

#####################################################################################################

@dataclass(frozen=True)
class _LocalizedSentence:
    default_text: str
    localized_sentences: Mapping[LKey, str] = field(default_factory=lambda: FrozenDict({}))

    #####################################################################################################

    def __call__(self, logger: Logger, locale: LKey = LKey.EN, **kwargs: str | int | bool) -> str:
        localized_sentence = self.localized_sentences.get(locale, '')
        if not localized_sentence:
            logger.warning(f'Cannot find localized sentence for "{locale.value}". Use default text: "{self.default_text}"')
            localized_sentence = _clean_notranslate_wraps(self.default_text)
        return localized_sentence.format(**kwargs)

#####################################################################################################

class TKey(_LocalizedSentence, Enum):
    LANG_SELECT_TITLE = 'Select your preferred language', _LANG_SELECT_TITLE_MAP
    DIALOG_PLACEHOLDER = 'Click on the microphone and start talking', _DIALOG_PLACEHOLDER_MAP
    END_DIALOG = 'End the dialog', _END_DIALOG_MAP
    START_DIALOG = 'Start the dialog', _START_DIALOG_MAP
    CLOSE_POPUP_TITLE = 'Would you like to end the dialog?', _CLOSE_POPUP_TITLE_MAP
    CLOSE_POPUP_TEXT = 'It will be impossible to return and continue the dialog after completion.', _CLOSE_POPUP_TEXT_MAP
    CLOSE_POPUP_END_BTN = 'End', _CLOSE_POPUP_END_BTN_MAP
    CLOSE_POPUP_CONTINUE_BTN = 'Сontinue the dialog', _CLOSE_POPUP_CONTINUE_BTN_MAP
    NEXT_SURVAY_BTN = 'Next', _NEXT_SURVAY_BTN_MAP
    SKIP_SURVAY_BTN = 'or Skip the survey', _SKIP_SURVAY_BTN_MAP
    QUESTION = 'Question', _QUESTION_MAP
    OF = 'of', _OF_MAP
    SURVAY_ONE_TITLE = 'Please rate on a scale from 1 to 5 how easy it was for you to use the translator.', _SURVAY_ONE_TITLE_MAP
    SURVAY_ONE_RATE_ONE = 'Very difficult', _SURVAY_ONE_RATE_ONE_MAP
    SURVAY_ONE_RATE_TWO = 'Difficult', _SURVAY_ONE_RATE_TWO_MAP
    SURVAY_ONE_RATE_THREE = 'Neutral', _SURVAY_ONE_RATE_THREE_MAP
    SURVAY_ONE_RATE_FOUR = 'Easy', _SURVAY_ONE_RATE_FOUR_MAP
    SURVAY_ONE_RATE_FIVE = 'Very easy', _SURVAY_ONE_RATE_FIVE_MAP
    SURVAY_TWO_TITLE = 'Please rate from 1 to 5 how likely you are to recommend our service to a friend or a colleague.', _SURVAY_TWO_TITLE_MAP
    SURVAY_TWO_RATE_ONE = 'Very Unlikely', _SURVAY_TWO_RATE_ONE_MAP
    SURVAY_TWO_RATE_TWO = 'Unlikely', _SURVAY_TWO_RATE_TWO_MAP
    SURVAY_TWO_RATE_THREE = 'Neutral', _SURVAY_TWO_RATE_THREE_MAP
    SURVAY_TWO_RATE_FOUR = 'Likely', _SURVAY_TWO_RATE_FOUR_MAP
    SURVAY_TWO_RATE_FIVE = 'Very Likely', _SURVAY_TWO_RATE_FIVE_MAP
    SURVAY_THREE_TITLE = 'Please rate the quality of translation on a scale from 1 to 5.', _SURVAY_THREE_TITLE_MAP
    SURVAY_THREE_RATE_ONE = 'Terrible', _SURVAY_THREE_RATE_ONE_MAP
    SURVAY_THREE_RATE_TWO = 'Bad', _SURVAY_THREE_RATE_TWO_MAP
    SURVAY_THREE_RATE_THREE = 'Normal', _SURVAY_THREE_RATE_THREE_MAP
    SURVAY_THREE_RATE_FOUR = 'Good', _SURVAY_THREE_RATE_FOUR_MAP
    SURVAY_THREE_RATE_FIVE = 'Perfect', _SURVAY_THREE_RATE_FIVE_MAP
    REVIEW_TITLE = 'Please share your thoughts about the service in general.', _REVIEW_TITLE_MAP
    REVIEW_PLACEHOLDER = 'Tap to start writing or record voice', _REVIEW_PLACEHOLDER_MAP
    REVIEW_BOTTOM_TEXT = 'You can skip this question and finish the survey straight away', _REVIEW_BOTTOM_TEXT_MAP
    FINISH_SURVAY_BTN = 'Finish the survey', _FINISH_SURVAY_BTN_MAP
    FINAL_TEXT = 'Thank you for your answers!', _FINAL_TEXT_MAP
    BACK_TO_MENU_BTN = 'Back to menu', _BACK_TO_MENU_BTN_MAP
    EDITING = 'Editing', _EDITING_MAP
    T_ARABIC = 'Arabic', _T_ARABIC_MAP
    T_AZERBAIJANI = 'Azerbaijani', _T_AZERBAIJANI_MAP
    T_GERMAN = 'German', _T_GERMAN_MAP
    T_ENGLISH = 'English', _T_ENGLISH_MAP
    T_SPANISH = 'Spanish', _T_SPANISH_MAP
    T_FRENCH = 'French', _T_FRENCH_MAP
    T_HINDI = 'Hindi', _T_HINDI_MAP
    T_KOREAN = 'Korean', _T_KOREAN_MAP
    T_NEPALI = 'Nepali', _T_NEPALI_MAP
    T_RUSSIAN = 'Russian', _T_RUSSIAN_MAP
    T_TAJIK = 'Tajik', _T_TAJIK_MAP
    T_URDU = 'Urdu', _T_URDU_MAP
    T_UZBEK = 'Uzbek', _T_UZBEK_MAP
    T_CHINESE = 'Chinese', _T_CHINESE_MAP
    T_TAGALOG = 'Tagalog', _T_TAGALOG_MAP
    T_HUNGARIAN = 'Hungarian', _T_HUNGARIAN_MAP
    T_PUNJABI = 'Punjabi', _T_PUNJABI_MAP
    LOGIN = "Login", _LOGIN_MAP
    PASSWORD = "Password", _PASSWORD_MAP
    SIGN_IN = "Sign in", _SIGN_IN_MAP
    ERR_LOGIN_MSG = "Incorrect login or password entered", _ERR_LOGIN_MSG_MAP
    REC_ERROR_MSG = 'Speech recognition failed. Please try again.', _REC_ERROR_MSG_MAP
    THE_USER = 'The user', _THE_USER_MAP
    HAS_MORE_THAN_ONE_SESSION = 'has more than one open session', _HAS_MORE_THAN_ONE_SESSION_MAP
    CLOSE_ALL_SESSIONS = 'Close all except the current', _CLOSE_ALL_SESSIONS_MAP
    LEAVE_ALL_SESSIONS_OPEN = 'Leave all sessions open', _LEAVE_ALL_SESSIONS_OPEN_MAP
    TOTAL_OPEN_SESSIONS = 'Total open sessions', _TOTAL_OPEN_SESSIONS_MAP
    LOGIN_TO_YOUR_ACCOUNT = 'Login to your account', _LOGIN_TO_YOUR_ACCOUNT_MAP

    # ADMIN PAGE LOCALIZATION
    A_NAME = "Name", _A_NAME_MAP
    A_ADDRESS = "Address", _A_ADDRESS_MAP
    A_TIME_ZONE = "Time zone", _A_TIME_ZONE_MAP
    A_FULL_NAME = "Full name", _A_FULL_NAME_MAP
    A_IS_ACTIVE = "Is active", _A_IS_ACTIVE_MAP
    A_ADMINISTRATOR = "Admin", _A_ADMINISTRATOR_MAP
    A_DEPARTMENT = "Department", _A_DEPARTMENT_MAP
    A_DEPARTMENT_UUID = "UUID of Department", _A_DEPARTMENT_UUID_MAP
    A_USER = "User", _A_USER_MAP
    A_USER_LOGIN = "User login", _A_USER_LOGIN_MAP
    A_SESSION_UUID = "Session UUID", _A_SESSION_UUID_MAP
    A_DIALOG_UUID = "Dialog UUID", _A_DIALOG_UUID_MAP
    A_LANGUAGE = "Language", _A_LANGUAGE_MAP
    A_NPS_SCORE = "NPS score", _A_NPS_SCORE_MAP
    A_TRANSLATION_SCORE = "Translation score", _A_TRANSLATION_SCORE_MAP
    A_USABILITY_SCORE = "Usability score", _A_USABILITY_SCORE_MAP
    A_DIALOG_START = "Dialog start", _A_DIALOG_START_MAP
    A_DIALOG_END = "Dialog end", _A_DIALOG_END_MAP
    A_DIALOG_DURATION = "Duration of dialogue", _A_DIALOG_DURATION_MAP
    A_METRIC = "Metric", _A_METRIC_MAP
    A_RESULT = "Result", _A_RESULT_MAP
    A_DESCRIPTION = "Description", _A_DESCRIPTION_MAP
    A_MESSAGE_UUID = "Message UUID", _A_MESSAGE_UUID_MAP
    A_CREATION_DATE = "Date of creation", _A_CREATION_DATE_MAP
    A_RECOGNIZED_TEXT = "Recognized text", _A_RECOGNIZED_TEXT_MAP
    A_EDITED_TEXT = "Edited text", _A_EDITED_TEXT_MAP
    A_AUDIO = "Audio", _A_AUDIO_MAP
    A_EDIT = "Edit", _A_EDIT_MAP
    A_DELETE = "Delete", _A_DELETE_MAP
    A_CREATE = "Create", _A_CREATE_MAP
    A_FILTER = "Filter", _A_FILTER_MAP
    A_RESET = "Reset", _A_RESET_MAP
    A_DOWNLOAD = "Download", _A_DOWNLOAD_MAP
    A_DOWNLOAD_ALL = "Download all", _A_DOWNLOAD_ALL_MAP
    A_FROM = "From", _A_FROM_MAP
    A_TO = "To", _A_TO_MAP
    A_SOURCE_LANGUAGE = "Source language", _A_SOURCE_LANGUAGE_MAP
    A_SOURCE_TEXT = "Source text", _A_SOURCE_TEXT_MAP
    A_NUMBER_OF_LINES = "Number of lines", _A_NUMBER_OF_LINES_MAP
    A_TRANSLATION_LANGUAGE = "Translation language", _A_TRANSLATION_LANGUAGE_MAP
    A_TRANSLATED_TEXT = "Translated text", _A_TRANSLATED_TEXT_MAP
    A_REFERENCE_TEXT = "Reference text", _A_REFERENCE_TEXT_MAP
    A_ANOTHER_TRANSLATOR = "Another translator", _A_ANOTHER_TRANSLATOR_MAP
    A_CALCULATE = "Calculate", _A_CALCULATE_MAP
    A_COMPARE_TRANSLATORS = "Compare translators", _A_COMPARE_TRANSLATORS_MAP
    A_RECOGNITION_SCORE = "Recognition quality score", _A_RECOGNITION_SCORE_MAP
    A_RECOGNITION_ERRORS = "Recognition errors", _A_RECOGNITION_ERRORS_MAP

    A_ERROR_CREATE_DEP = "Error while creating department.", _A_ERROR_CREATE_DEP_MAP
    A_ERROR_EDIT_DEP = "Error while editing department.", _A_ERROR_EDIT_DEP_MAP

    A_BASE_ERROR_DELETE_USER = "Error while deleting user", _A_BASE_ERROR_DELETE_USER_MAP
    A_ERROR_DELETE_USER = "It is impossible to delete a user because there are dialogs linked to this user.", _A_ERROR_DELETE_USER_MAP
    A_ERROR_EDIT_USER = "Cannot edit. User not found.", _A_ERROR_EDIT_USER_MAP
    A_ERROR_CREATE_USER = "Error creating user.", _A_ERROR_CREATE_USER_MAP
    A_CONFIRM_DELETE_USER = "Are you sure you want to delete the user ", _A_CONFIRM_DELETE_USER_MAP
    A_DIALOGS_COUNT = "Dialogs count:", _A_DIALOGS_COUNT_MAP

    A_CONFIRM_DELETE_CONV = "Are you sure you want to delete this dialog?", _A_CONFIRM_DELETE_CONV_MAP
    A_ERROR_DELETE_CONV = "Error while deleting dialog", _A_ERROR_DELETE_CONV_MAP
    A_USER_DEL_HIMSELF = "The user cannot delete himself.", _A_USER_DEL_HIMSELF_MAP

    A_DEP_NAME_EMPTY = "Department name cannot be empty.", _A_DEP_NAME_EMPTY_MAP
    A_INCORRECT_TIME_ZONE = "Invalid time zone format.", _A_INCORRECT_TIME_ZONE_MAP

    A_UNABLE_TO_DELETE_DEP = "It is impossible to delete a department because users are linked to it", _A_UNABLE_TO_DELETE_DEP_MAP
    A_UNABLE_TO_EDIT = "Unable to edit. Department not found.", _A_UNABLE_TO_EDIT_MAP

    # download conversation headers
    A_OPERATOR_NAME = "Operator name", _A_OPERATOR_NAME_MAP
    A_AUDIO_UUID = "Audio UUID", _A_AUDIO_UUID_MAP
    A_MESSAGE_TYPE = "Message type", _A_MESSAGE_TYPE_MAP
    A_MESSAGE_START = "Message start at", _A_MESSAGE_START_MAP
    A_TARGET_LANGUAGE = "Target language", _A_TARGET_LANGUAGE_MAP
    A_EDITING_TIME = "Editing time", _A_EDITING_TIME_MAP

    # Metrics pages
    M_AVERAGE = "average", _M_AVERAGE_MAP
    M_AVERAGE_SCORE = "Average score", _M_AVERAGE_SCORE_MAP
    M_STANDARD_DEVIATION = "Standard deviation", _M_STANDARD_DEVIATION_MAP
    M_MINIMUM_VALUE = "Minimum value", _M_MINIMUM_VALUE_MAP
    M_MAXIMUM_VALUE = "Maximum value", _M_MAXIMUM_VALUE_MAP
    M_MEDIAN = "Median", _M_MEDIAN_MAP
    M_ANOTHER_TRANSLATOR_AVERAGE = "Another translator average", _M_ANOTHER_TRANSLATOR_AVERAGE_MAP
    M_AVERAGE_DIFFERENCE = "Average difference", _M_AVERAGE_DIFFERENCE_MAP
    M_CONFIDENCE_INTERVAL = "Confidence interval of the difference", _M_CONFIDENCE_INTERVAL_MAP
    M_SIGNIFICANT_DIFFERENCE = "Significant difference", _M_SIGNIFICANT_DIFFERENCE_MAP
    M_SELECT_LANG = "Select language", _M_SELECT_LANG_MAP
    M_INPUT_EMPTY = "The input field cannot be empty.", _M_INPUT_EMPTY_MAP
    M_REFERENCE_EMPTY = "The reference text input field cannot be empty.", _M_REFERENCE_EMPTY_MAP
    M_DIFFERENT_NUMBER = "Different number of source and translated lines.", _M_DIFFERENT_NUMBER_MAP
    M_REF_DIFFERENT_NUMBER = "The number of reference lines does not match the original.", _M_REF_DIFFERENT_NUMBER_MAP
    M_TRANSLATOR_DIFFERENT_LINES = "The number of lines of another translator does not match the original one.", _M_TRANSLATOR_DIFFERENT_LINES_MAP
    M_TABLE_QUALITY = "Translation quality assessment results table.", _M_TABLE_QUALITY_MAP
    M_METRICS_COMPLETED = "Translation quality assessment completed.", _M_METRICS_COMPLETED_MAP
    M_METRICS_ERROR = "Translation quality assessment error.", _M_METRICS_ERROR_MAP
    M_WIP = "The metric shows the percentage of information saved in the recognized text.", _M_WIP_MAP
    M_WIL = "The metric shows the percentage of lost information in the recognized text.", _M_WIL_MAP
    M_WER = "Percentage of errors in word recognition.", _M_WER_MAP
    M_MER = "A modification of WER where only substitutions and insertions are observed.", _M_MER_MAP
    M_CER = "Similar to WER, but applies to characters instead of words.", _M_CER_MAP
    M_JER = "A metric based on the Jaccard distance.", _M_JER_MAP
    M_RECOGNITION_ERROR = "Error calculating recognition metrics", _M_RECOGNITION_ERROR_MAP

    # Metrics descriptions
    M_COMET_20_DESC = (
        '"COMET-20-QE" is a metric for assessing the quality of translation'
        ' using trained neural network models without a reference translation.'
    ), _M_COMET_20_DESC_MAP
    M_COMET_22_DESC = (
        '"COMET-22-DA" is a metric for assessing the quality of translation using'
        ' trained neural network models.'
    ), _M_COMET_22_DESC_MAP
    M_BLEU_DESC = (
        '"BLEU" is a metric for assessing the quality of translation by counting the coincidence'
        ' of word combinations in the reference translation.'
    ), _M_BLEU_DESC_MAP
    M_SONAR_DESC = (
        '"SONAR" - a metric for assessing the quality'
        ' of translation using neural network models without a reference translation'
    ), _M_SONAR_DESC_MAP
    M_CONF_INTERVAL_DESC = (
        '"Confidence interval of the difference in means" - is constructed using the bootstrap statistical method.'
        ' To construct a correct confidence interval, the following prerequisites must be met:'
        '- the sample must be representative (i.e. translations must be presented for different products/departments;'
        ' sentences must be of different lengths (short, medium, long); '
        '- the test size is preferably 300 lines or more (with a small test size, 100 lines or less,'
        ' the confidence interval will be quite narrow and may not capture the true value of the difference)'
    ), _M_CONF_INTERVAL_DESC_MAP
    M_ALPHA_DESC = (
        '"ALPHA" - significance level; alpha = 0.05 means that with a probability of 95%'
        ' the true value of the difference in means will be within the confidence interval.'
        ' The probability that the true value of the difference in means will be outside the confidence interval will be 5%.'
    ), _M_ALPHA_DESC_MAP
    M_P_VAL_DESC = (
        '"P-VALUE" - the probability that the difference between the means will be zero; compared with the significance level alpha.'
        ' If the p-value is greater than or equal to alpha, this means that we have no reason to reject the null hypothesis'
        ' (the translation quality of the two systems is equivalent). If the p-value is less than alpha, '
        'the null hypothesis is rejected (the quality of the two systems differs).'
    ), _M_P_VAL_DESC_MAP
    M_STD_DEV_DESC = (
        '"Standard Deviation" - shows how widely the values in the data are scattered relative to their mean.'
    ), _M_STD_DEV_DESC_MAP
    M_MEDIAN_DESC = (
        'Median is a measure that divides a set of data into two equal halves. Half of the data is less than the median, and half of the data is greater than the median.'
    ), _M_MEDIAN_DESC_MAP
    M_IQR_DESC = '"IQR" (Interquartile Range) - shows the range in which 50% of the data lies.', _M_IQR_DESC_MAP

    A_CANCEL = "Cancel", _A_CANCEL_MAP
    A_APPROVE_DELETION = "Are you sure you want to delete the department", _A_APPROVE_DELETION_MAP
    A_YES = "Yes", _A_YES_MAP
    A_NO = "No", _A_NO_MAP
    A_CLOSE = "Close", _A_CLOSE_MAP
    A_REQUIRED_FIELDS = "Fields are required.", _A_REQUIRED_FIELDS_MAP
    A_WRONG_DATE_FORMAT = "Invalid date format.", _A_WRONG_DATE_FORMAT_MAP
    A_PASSWORD_EMPTY = "Password cannot be empty", _A_PASSWORD_EMPTY_MAP
    A_LOGIN_EMPTY = "Login cannot be empty", _A_LOGIN_EMPTY_MAP
    A_FULL_NAME_EMPTY = "Full name cannot be empty", _A_FULL_NAME_EMPTY_MAP
    A_SELECT_DEPARTMENT = "Select department", _A_SELECT_DEPARTMENT_MAP
    A_NEW_USER_PASSWORD = "New password", _A_NEW_USER_PASSWORD_MAP
    A_DATE_VALIDATION = "The start date cannot be later than the end date.", _A_DATE_VALIDATION_MAP
    A_DOWNLOAD_FORMAT = "File format", _A_DOWNLOAD_FORMAT_MAP
    A_DOWNLOAD_AUDIO = "Download audio", _A_DOWNLOAD_AUDIO_MAP

    # Multiple
    A_DEPARTMENTS = "Departments", _A_DEPARTMENTS_MAP
    A_USERS = "Users", _A_USERS_MAP
    A_DIALOGS = "Dialogs", _A_DIALOGS_MAP
    A_TRANSLATION_METRICS = "Translation metrics", _A_TRANSLATION_METRICS_MAP
    A_RECOGNITION_METRICS = "Recognition Metrics", _A_RECOGNITION_METRICS_MAP

#####################################################################################################
