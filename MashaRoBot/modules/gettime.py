import datetime
from typing import List

import requests
from MashaRoBot import TIME_API_KEY, dispatcher
from MashaRoBot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async


def generate_time(to_find: str, findtype: List[str]) -> str:
    data = requests.get(
        f"https://api.timezonedb.com/v2.1/list-time-zone"
        f"?key={TIME_API_KEY}"
        f"&format=json"
        f"&fields=countryCode,countryName,zoneName,gmtOffset,timestamp,dst"
    ).json()

    for zone in data["zones"]:
        for eachtype in findtype:
            if to_find in zone[eachtype].lower():
                country_name = zone["countryName"]
                country_zone = zone["zoneName"]
                country_code = zone["countryCode"]

                if zone["dst"] == 1:
                    daylight_saving = "Iya"
                else:
                    daylight_saving = "Tidak"

                date_fmt = r"%d-%m-%Y"
                time_fmt = r"%H:%M:%S"
                day_fmt = r"%A"
                gmt_offset = zone["gmtOffset"]
                timestamp = datetime.datetime.now(
                    datetime.timezone.utc
                ) + datetime.timedelta(seconds=gmt_offset)
                current_date = timestamp.strftime(date_fmt)
                current_time = timestamp.strftime(time_fmt)
                current_day = timestamp.strftime(day_fmt)

                break

    try:
        result = (
            f"🗺️<b>Negara:</b> <code>{country_name}</code>\n"
            f"🖊️<b>Nama Zona:</b> <code>{country_zone}</code>\n"
            f"📟<b>Kode Negara:</b> <code>{country_code}</code>\n"
            f"🔅<b>Hemat Siang Hari:</b> <code>{daylight_saving}</code>\n"
            f"💠<b>Hari:</b> <code>{current_day}</code>\n"
            f"⏲️<b>Waktu Saat Ini:</b> <code>{current_time}</code>\n"
            f"🗓️<b>Tanggal Hari ini:</b> <code>{current_date}</code>\n"
            '🌏<b>Zona Waktu:</b> <a href="https://id.wikipedia.org/wiki/Daftar_zona_waktu">Lihat Daftar</a>'
        )
    except:
        result = None

    return result


@run_async
def gettime(update: Update, context: CallbackContext):
    message = update.effective_message

    try:
        query = message.text.strip().split(" ", 1)[1]
    except:
        message.reply_text("Provide a country name/abbreviation/timezone to find.")
        return
    send_message = message.reply_text(
        f"<i>Mencari informasi waktu untuk wilayah</i> <b>{query}</b>", parse_mode=ParseMode.HTML
    )

    query_timezone = query.lower()
    if len(query_timezone) == 2:
        result = generate_time(query_timezone, ["countryCode"])
    else:
        result = generate_time(query_timezone, ["zoneName", "countryName"])

    if not result:
        send_message.edit_text(
            f"<i>Informasi waktu untuk wilayah</i> <b>{query}</b> <i>tidak ditemukan</i>.\n"
            '<b>Daftar Zona Waktu:</b> <a href="https://id.wikipedia.org/wiki/Daftar_zona_waktu">lihat disini</a>',
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True,
        )
        return

    send_message.edit_text(
        result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
    )


__help__ = """
 ❍ /time <intruksi>*:* menampilkan informasi waktu
*Intruksi yang tersedia:* Kode Negara/Nama Kota/Nama Zona Waktu
 ❍ ⏰ [Daftar Zona Waktu](https://id.wikipedia.org/wiki/Daftar_zona_waktu)
💡 Contoh:- /time Id *:* untuk melihat informasi waktu dan tanggal negara Indonesia..
"""

TIME_HANDLER = DisableAbleCommandHandler("time", gettime)

dispatcher.add_handler(TIME_HANDLER)

__mod_name__ = "Waktu"
__command_list__ = ["time"]
__handlers__ = [TIME_HANDLER]
