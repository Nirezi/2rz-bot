hyojun_help = [
    {"name": "/(s,m,h)timer time content",
     "value": "タイマー用コマンド",
     "info": "指定された時間後メンション付きのメッセージを送ります\nsなら秒、mなら分、hなら時間でタイマーの時間を指定できます。なお小数点にも対応しています(botの再起動時にリセットされます)",
     "image": "None"},
    {"name": "/role_count id",
     "value": "roleを持っているユーザーの数を表示します",
     "info": "特に説明することなし！",
     "image": "None"},
    {"name": "/role_info id",
     "value": "roleの詳細な情報を表示します",
     "info": "特に説明することなし！",
     "image": "None"},
    {"name": "/members",
     "value": "実行された鯖にいるユーザーを表示します。",
     "info": "ユーザーの数によっては表示されないことがあります(6000文字を超えると送信できません)",
     "image": "None"},
    {"name": "/myrole",
     "value": "実行者の持っているroleを表示します。",
     "info": "特に説明することなし！",
     "image": "None"},
    {"name": "/roles",
     "value": "実行された鯖にあるroleを表示します",
     "info": "特に説明することなし！",
     "image": "None"},
    {"name": "/bug_report",
     "value": "本botのバグ報告用のコマンドです",
     "info": "かなりログが流れてしまうためコマンド用のチャンネルで実行することを推奨します",
     "image": "None"},
    {"name": "/dm",
     "value": "botがdmに凸ります。spamです",
     "info": "ラグでまれに順番がおかしくなることがあります。また連続で実行するとおかしいことになります",
     "image": "None"},
    {"name": "/guilds",
     "value": "本botが参加している鯖を表示します",
     "info": "特に説明することなし！",
     "image": "None"},
    {"name": "/bot_info",
     "value": "本botの詳細を表示します",
     "info": "それだけのコマンド。需要がないとかいわないで()",
     "image": "None"},
    {"name": "/weather 地点",
     "value": "指定した地点の天気を表示します。",
     "info": "参照できる地点は/titenコマンドで見ることができます",
     "image": "None"},
    {"name": "/titen",
     "value": "天気を参照できる地点を表示します",
     "info": "見にくいのは許して()",
     "image": "None"},
    {"name": "/avatar id",
     "value": "ユーザー、もしくは鯖のアバターを表示します",
     "info": "標準のアイコンを使っている鯖の場合表示されません。(仕様だからゆるして)",
     "image": "None"},
    {"name": "/vote title 候補",
     "value": "投票を取るよ！",
     "info": "第一引数に投票のタイトル、第二引数以降に候補を渡してね！！！！。候補が一つだと:o::x:で投票を取るぞ！",
     "image": "None"},
    {"name": "/help",
     "value": "これを表示します",
     "info": "使いやすくしたつもりです。褒めて()",
     "image": "None"}
]

shiba_help = [
    {"name": "/join",
     "value": "企画用の役職付与",
     "info": "企画の期間中に実行すると企画用の役職が付与されます。指定チャンネル以外で実行すると怒られます",
     "image": "None"},
    {"name": "/ch",
     "value": "たこしばスタジオのurlを表示",
     "info": "実行するとたこしばスタジオのurlを表示します。見てね！！！！",
     "image": "None"},
    {"name": "/studio",
     "value": "スタジオのツイッターurlを表示",
     "info": "実行するとスタジオのツイッターを表示します",
     "image": "None"},
    {"name": "/(riku,tako,iroha,shiba)",
     "value": "メンバーのツイッターのurl表示",
     "info": "それぞれ対応したメンバーのツイッターurlを表示します\n~~2レジのは恥ずかしいのでないです~~",
     "image": "None"},
]

help_2rz = [
    {"name": "/test",
     "value": "2rzのテスト用コマンド",
     "info": "やってみると何かテストの残骸があるかも、、？(多分しょぼい)",
     "image": "None"},
    {"name": "/mcid user_id",
     "value": "指定した人のmcid表示機能",
     "info": "指定した人のmcidを表示します。(需要ないとか言わないでください)",
     "image": "None"}
]

help_ohatsu = [
    {"name": "/(ohatsu,build,mine)",
     "value": "指定した役職の付与、剥奪",
     "info": "指定した役職の付与、剥奪をします。トグル式になっています",
     "image": "None"}
]

help_dic = {
    628182826914676758: shiba_help,  # しばさんのとこ
    615394790669811732: shiba_help,  # しばさんのとこ2
    621326525521723414: help_2rz,  # 2レジ鯖
    612401848787140656: help_ohatsu,  # お初鯖
}
