import os
import asyncio
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT1_TOKEN = os.getenv("BOT1_TOKEN")
BOT2_TOKEN = os.getenv("BOT2_TOKEN")

group_chat_id = None
chat_started = False

# Story-based role-play between Naruto and Hinata (dialogue pairs)
story_sequence = [

("damn this place is deep… trees everywhere 😮", "yeah it’s like a dream 🌿 so quiet too 😊"),

("lowkey feels like we're the only ppl on earth rn 😌", "i like that… just u n me 🥺"),

("u brought the snacks right? 😆", "ofc i did! u think i’d let u starve? 😝"),

("ur the besttt *grabs her hand* come on let’s go deeper in 💞", "*blushes* ur hand’s warm… i like holdin it 😚"),

("u always say stuff like that n make my heart beat dumb fast 😩", "then imagine how mine feels rn 🙃"),

("*laughs n bumps her gently* ur too cute i swear 😁", "*leans on him a bit* don’t let go ok ☺️"),

("never gonna let go… ever 🥲", "*rests head on his shoulder* i feel so safe here 🫠"),

("this tree got like glowing moss or smth?? 😳", "omg it's beautiful 😮 take a pic!!"),

("nahh rather look at u than take pics 🤭", "smooooth talker 😏 u tryna get kissed?"),

("maybe 😝", "*grabs his face n kisses him soft n slow* 😚"),

("....damn hina", "*giggles* what? u said maybe 😘"),

("i wasn’t ready but damn... do it again 😩", "*smirks* u gotta earn it now 😌"),

("what if i carried u over that log n didn’t put u down til u kissed me again 😏", "then i’m def not walkin again today 😗"),

("aight bet *lifts her up bridal style* u asked for it 😉", "*wraps arms round his neck* u love carrying me huh 🤭"),

("not gonna lie yeah... u feel perfect in my arms 🫠", "*rests her cheek on his chest* keep talkin like that n i’ll melt fr 😵‍💫"),

("yo look at that huge flower 😮", "woah it smells sooo sweet 🥹 wanna pick one?"),

("nah imma leave it... wild things are better untouched 🙃", "*looks at him* u really think that?"),

("yeah… like u… wild n beautiful 😌", "*face turns red* stoppp u makin me shy 😖"),

("no chance… u mine n i’m proud 😤", "*laughing soft* u a whole romantic out here 💕"),

("only for u hina... only ever u 💞", "*smiles big n kisses his cheek* u makin me fall more every sec 😙"),

("yo hina... u hear that water? think there’s a stream nearby 🤨", "ooh maybe we can dip our feet in 😚"),

("let’s check it out *pulls her along with a grin* 😁", "*laughs* ur always so hyped, i love it 😆"),

("bruh this place lowkey magical… look at that water sparkle 💦", "it’s sooo clear omg 😮 like a dream 💕"),

("*takes off sandals n dips feet* ahhh this feel gooddd 🥵", "*joins in* omg yesss this is heaven 😩"),

("*splashes her a little* 😝", "hey! 😖 *splashes back n giggles* ur dead now 😝"),

("nahh u missed 🤭 try again", "*sneaky* or maybe i’ll just grab u n pull u in 😏"),

("oh snap *stumbles n falls into her arms* okay okay i surrender 😆", "*wraps arms around him* now u stuck here 🤗"),

("not complainin at all… *looks in her eyes* u so close rn 😗", "*leans in* u gon kiss me or just stare all day? 😉"),

("*kisses her hard this time, hands on her waist* 💞", "*presses closer, lips soft but deep* mmm 😚"),

("*pulls back slow* u taste like heaven fr 😮‍💨", "*smiling* that’s bc i been saving all my kisses for u 😙"),

("bruh... why u so perfect 😩", "not perfect... just perfectly urs ☺️"),

("*lays back on the grass near the stream* let’s chill here for a bit 😌", "*curls up next to him* u make the best pillow 🥹"),

("*wraps arm around her tight* better than a sleeping bag huh 😁", "1000x better 🫠 ur heartbeat makes me feel safe"),

("can’t stop kissin u fr 😫", "*smirks* then don’t... i ain’t stoppin u 😏"),

("*kisses her neck soft* that ok? 😗", "*shivers* mmm yeah... i like that a lot 😩"),

("u smell so good hina... like flowers n home 🥺", "*blushing hard* narutooo 🫣 ur gonna kill me"),

("nah i’m just tryna love u right 💕", "*leans into him more* u already do... more than u know 😚"),

("*soft laugh* we really out here in the jungle makin out 😆", "n lovin every sec of it 😝"),

("remind me to thank tsunade for this mission 😏", "*giggling* sameee omg this the best 'mission' ever 😄"),

("yo... if we build a lil hut here we could just stay forever 😮", "*pretending to think* hmm no work, just us, kisses, cuddles… deal 😌"),

("we’d run outta food tho 😐", "pffft not if i pack the snacks 😁 i’m always thinkin ahead"),

("ok u win *pulls her into lap* lemme thank u properly 😘", "*wraps arms round his neck* then do it slow... make it count 😚"),

("*resting against the tree* can’t believe how calm it is here 😌", "*lays head on his chest* it’s like the world paused for us 🥹"),

("if it did... i’d stay right here forever 🫠", "me too... just like this... with u ❤️"),

("*fingers tracing her arm slow* u gettin goosebumps or is that me 😏", "*soft giggle* nah that’s u bein dangerous 😩"),

("dangerous huh? what if i kissed u all over till u couldn’t think straight 😝", "*blushing* u wouldn’t… unless? 😳"),

("bet *starts kissin her shoulder slow n warm* 😚", "*gasps soft* naruto… ur really doin it 😫"),

("told u… jungle got me feelin wild af 🥵", "*buries face in his neck* mmm i love this side of u 😙"),

("i love every inch of u hina… inside n out 💞", "*grabs his shirt tight* stoppp ur makin my heart cry happy 😭"),

("*looks in her eyes* i just wanna drown in u rn fr 😩", "then come closer… no space left between us 😮‍💨"),

("*pulls her into his lap again* like this? 😗", "*nuzzles close* yeah… now kiss me slow again 😚"),

("*kisses her like the world’s ending* 💦", "*fingers tangled in his hair* omg… keep goin 😖"),

("*pauses* damn we really bout to make this jungle steam 😆", "*laughing* i swear u such a perv sometimes 😝"),

("only for u tho 😏 u bring it outta me hina", "*grinning* good. i want all of u... the soft n the wild 😌"),

("even the part that wanna carry u into the trees n steal u away forever? 😳", "*bites lip* yes pls. i’d let u 😩"),

("damn… sayin that do things to me 😬", "*leans in close* good. now imagine what i wanna do 😏"),

("u tryna test me huh", "test? nah babe… i’m passin u with flyin colors 😝"),

("*laughs hard* u got jokes and looks… unfair 😆", "*winks* and i got u. that’s the best flex 😌"),

("yo that rock over there shaped like a heart 😮", "*gasps* omg it is!!! it’s a sign fr 💞"),

("we should sit there. make it our love rock or smth 🤭", "*already walkin* u read my mind 😁"),

("*sits close* this rock got history now… first jungle makeout spot 😝", "*leans into him* first of many 😏"),

("wait… u plannin on more? 😳", "hell yeah… every tree gonna have our memories 😆"),

("u naughty lil thing 😩", "*innocent look* who me? i’m sweet af 😇"),

("sweet n spicy… dangerous combo 😝", "*soft voice* only for u… always for u 😌"),

("yo i’m not even thinkin bout leavin this place 😩", "me either… can we just stay one more night out here? 🥺"),

("say less. i’ll build us a blanket fort from leaves if i gotta 😁", "*laughing* omg i love u soooo much rn 💞"),

("*lays down on the heart rock* u comfy? 😌", "*lays beside him* with u? always 🥹"),

("this the part where we just stare at the stars n talk deep huh 🤭", "*nods* yeah... tell me sumthin u never told anyone ☺️"),

("*thinks* hmm... i used to dream about kissin u back in the academy 😳", "*gasps* no wayyy 😝 i had dreams like that too 🫠"),

("fr?? what we doin in those dreams huh 😏", "*covers face* i ain’t sayin... but i woke up blushing HARD 😩"),

("damn hinaaaaa *laughs* u wildin even in ur sleep 😝", "*smirks* and now it’s real... dream come true huh? 😙"),

("best dream ever... better than ramen i swear 😆", "oh woww now i KNOW u serious 😳"),

("*pulls her close* come here dream girl 💞", "*snuggles into him* u feel like home 😌"),

("*kisses her forehead soft* i’ll be ur home forever 🫡", "*smiles big* hold me tighter then... never let go 😚"),

("*arms lock around her* gotchu for life 😌", "*quiet voice* naruto... i love u so much it hurts sometimes 🥺"),

("don’t cry 😟 u gon make me tear up too 😖", "*wipes eyes* srry i just... never thought i’d feel this loved 💕"),

("u deserve ALL of it. every kiss, every hug, every dirty thought too 😏", "*laughing* ur so bad omg 😝 but i love it 😗"),

("speakinn of... i been holdin back 😬", "holding back what 👀"),

("*leans in n whispers* tryna kiss every inch of u under these stars tonight 😩", "*face red* narutooo u tryna ruin me out here 😭"),

("nah... tryna worship u 🥵", "*clings to him* say that again... slower this time 😫"),

("*in her ear* i. wanna. worship. u. hina. every. piece. 😩", "*shivers hard* stoppp i’m not gonna survive this 🫠"),

("then let’s die in each other’s arms rn 😝", "*giggling* okay but like... slowly 😌"),

("slow is my specialty 😏", "*innocent blink* i’m not stoppin u 😝"),

("yo u hear that owl? 😳", "*laughing* even the animals tryna spy on us now 😆"),

("pervy owl lmao 😆", "*lays back* at least he saw love in its rawest form 😌"),

("yooo we should name him kakashi jr 😝", "*laughing way too hard* ur soooo wrong for that 🤭"),

("man... i love u hina. not just the kissin n touchin... but u. all of u 🥹", "*smiles soft* and i love the way u see me… it’s like i finally see me too 😔"),

("*holds her close* no one else gets to see u like this but me 😏", "*kisses him slow* lucky u then 😗"),

("nahhh lucky US 😘", "*grinning* damn right ❤️"),

("yo hina... that flower glows in the dark 😮", "*leans in close* woahhh it’s so pretty omg 😯"),

("not as pretty as u tho 😌", "*blushing hard* bruhh stoooppp 😝"),

("no fr… nature tryna compete but u still winning 😏", "*giggles* i swear u got a flirting jutsu 🤭"),

("only activates when ur around 😉", "*smirks* so it’s always on then huh?"),

("basically 😁 u got me actin up 24/7", "*lays hand on his chest* i like that… makes me feel special 🥺"),

("*grabs her hand n kisses her knuckles* bc u are... my whole world hina 💞", "*shivers* god i love when u talk like that 😫"),

("what if we made this spot ours forever... like come back every year just us 🥹", "yes pls... a lil secret place just for our love 🫠"),

("*smiles soft* imagine bringin our future lil ones here too ☺️", "*eyes wide* wait— u seein kids with me?? 😳"),

("hell yeah... u n me? perfect team. perfect parents 💕", "*teary eyed smile* omg naruto 😭 u really see forever with me?"),

("i been saw it... since u first looked at me all shy back then 🥲", "*leans in* c’mere... lemme kiss u like forever’s already ours 😚"),

("*pulls her into a long deep kiss* 💞", "*wraps arms round him tight* mmm... don’t stop yet 😩"),

("never stoppin. not with u. not ever 😌", "then take ur time... i’m all yours 😗"),

("*whispers in her ear* wanna hear u say my name again n again tonight 😏", "*soft moan* narutoooo... u really tryna make me lose it 😖"),

("yep. gonna kiss u til the moon jealous 😝", "*laughing* god u cheesy af... n i love it 😆"),

("*grins* cheesy ninja love style baby 😁", "*grabs his face* come here cheese ball *kisses* 😘"),

("*sighs happy* bruh how u make my heart feel like it’s floatin 😌", "bc mine’s doin the same thing 🥲"),

("yo... if we fall asleep out here u think some forest spirit gon bless our love or smth 🤭", "*smiles* maybe it already did... look at us 🥹"),

("fr. this whole trip feel like destiny or sum 😮", "*snuggles up* it’s fate. us. here. now. forever ❤️"),

("*yawns* lowkey gettin sleepy but i don’t wanna stop holdin u 😴", "*giggles* sameee... stay like this til we pass out 😌"),

("aight bet *pulls her closer* jungle sleep mode activated 🤗", "*rests forehead on his* goodnight love 😙"),

("goodnight baby... dream of us 💞", "*whispers* i always do 😚"),

("*hours later* yo hina... u still awake? 😳", "*groggy* mm kinda... what’s up?"),

("just wanted to say... i never been this happy in my whole damn life 🥹", "*smiles in the dark* me neither naruto... me neither 😔"),

("*morning hits* damn... u still sleepin? 🥺", "*stirs* mmm not anymore... good morning love 😚"),

("*kisses her forehead* morning sunshine ☀️", "*smiles* u warm... like my favorite blanket 😌"),

("yo i think a bird tried to poop on me 😑", "*laughing hard* omg naruto stooop 😆"),

("i’m dead serious 😐 lil dude was aiming 💀", "*snorts* nature’s revenge for last night’s jungle sins 😝"),

("*grinning* worth every sec tho 😏", "*leans over n kisses him* damn right it was 😙"),

("we should wash up in the stream again… u know... fresh start 😉", "*eyebrow raise* fresh n frisky huh 😝"),

("maybeee *shrugs with innocent face* 😬", "*giggles* i’m in... race u there 😆"),

("*starts runnin* last one’s a soggy ramen noodle!! 😁", "*laughing n chasing* u better not beat meee 😝"),

("*jumps in stream clothes n all* WOOO 💦", "*splash* omg narutooo u crazyyy 😖"),

("crazy for u maybe 😏", "*swims up close* u a mess... but u my mess 😚"),

("*pulls her into arms in the water* god ur skin’s soft even in cold water 😩", "*wraps legs round his waist* keep touchin then 😏"),

("yo hinaaaa *voice cracking* u tryna end me rn 😭", "*whispers* maybe… or maybe i’m tryna make u feel alive 🫠"),

("*deep breath* u do both at once... wild lil goddess 😮‍💨", "*grins soft* and u my wild ninja king 😌"),

("*kisses her in the water* this feel like a movie fr 💞", "nah... this OUR movie 😚 and it’s R-rated 😝"),

("yo i can’t stop smilin like an idiot around u 😁", "*kisses his cheek* good. ur smile’s my fav thing ever ☺️"),

("aight let’s dry off n go deeper in... i saw a cave up that hill 😳", "ooooh cave date?? spooky sexy vibe? 😏"),

("exactly *winks* u know the drill 😆", "*laughs* let’s get it then 🫡"),

("*walking up trail* lowkey this hill steeper than i thought 😩", "*huffin* ughh my legs bout to quittt 😫"),

("*grabs her hand* hop on my back then princess 💪", "*climbs on* u just wanted me on ur back huh 😝"),

("caught me. i like feelin u close 😏", "*nuzzles his neck* i like it too... keep goin strongman 😚"),

("*reaches cave* aight we here... this place cold af tho 🥶", "*wraps arms round him* then warm me up baby 🥵"),

("say less 😏 *starts kissin her neck again* we bringin heat to this cave rn", "*moaning soft* mmm narutooo... i’m already melting 🫠"),

("imagine if someone walk in rn 😳", "*laughing* they gon learn what love look like up close 🤭"),

("lmao u nasty 😆", "only when i’m with u 😉"),

("yo i might not make it out this cave alive... death by kissin 😩", "*grinning* what a way to go tho 😗"),

("*layin on his chest in the cave* i can hear ur heartbeat 😌", "*soft smile* that’s bc it’s beatin just for u 😚"),

("yo... u ever think bout what it’d be like if we never got together? 😕", "*eyes widen* don’t say that... that’s my nightmare 😩"),

("fr mine too... life would be so damn gray without u 😔", "*tracing his chest* but we found each other... that’s all that matters now ❤️"),

("u really changed my life hina... i never felt this seen before 😞", "*whispers* i see every part of u... even the ones u hide from everyone else 🥺"),

("*leans in slow* u always make me feel like i’m enough... even when i’m broken 😖", "*kisses him gentle* bc u are... even broken u’re beautiful to me 💞"),

("damn girl... how u healing my soul with a kiss 😮‍💨", "*grinning* it’s called love... deep, messy, real love 😗"),

("*wraps arms round her tight* i’m never lettin that go 😤", "*nuzzles in* good. hold me forever 😚"),

("yo... i’m lowkey feelin bold rn 😏", "*raises brow* bold like... wild naruto mode again? 😝"),

("bold like i wanna see how loud u can get in this echo cave 😳", "*covers face* omgggg u tryna embarrass me 😫"),

("*grins* nahhh just tryna hear u sing my name 😩", "*smirks* then earn it baby 😏"),

("*leans down* challenge accepted *kisses her deep* 😙", "*soft gasp* damn naruto... u serious serious huh 🫠"),

("when it comes to u? always 😌", "*whispers* then don’t stop... not now... not ever 😖"),

("*hours later* u good? u look like jelly rn 😆", "*laughin weak* u drained me ninja 😩"),

("worth it tho? 😁", "*smiles tired* every second... every kiss... every moan 🥵"),

("*lays beside her* imma write about this in my mind forever 🥹", "same... this cave? our lil secret forever 😗"),

("yo... i think i love this jungle more than the village rn 😬", "*laughing* bc this jungle let u be a full perv huh 😝"),

("nahhh... it let me be *me*... no mask, no stress... just love 😔", "*nods slow* and i love *all* of u. even the parts u think u gotta hide 🥲"),

("*soft grin* swear u my heart’s safe place hina 💞", "*blushin* then i’ll protect it like my life depends on it 😤"),

("*sits up slow* ok so real talk... we bringin a hammock next time right? my back lowkey cryin 😩", "*laughing* i’ll bring two 😝 one for cuddles... one for chaos 😏"),

("yoooo u nasty 😆 i like it", "*smirks* i learned from the best 😉"),

("aight... cave love session = complete. what’s next? 🤭", "*thinking* maybe... jungle hot spring? 👀"),

("don’t play with me girl 😳 that sounds like the dream spot", "*smiles* then follow me love... we got more memories to make 💕"),

("*starts packin up* swear this trip the best thing ever happened to me 🥹", "*hugs from behind* me too... this changed everything 😌"),

("*walking hand in hand* yo u hear that? sounds like water 😮", "*perks up* omg that’s the hot spring ain’t it?? 😆"),

("*grinning* c’monnn we gotta see this rn 😁", "*runs ahead* last one there’s a soggy kunai 😝"),

("*reaches spring* YO. this place look like paradise 🥹", "*gasps* it’s steaming... flowers... even lil lights... wow 😍"),

("look at all this mist... lowkey feelin like a fantasy novel rn 😌", "*smirks* so who u gon be? steamy jungle prince? 😏"),

("*pulls shirt off* call me hot spring hokage 😆", "*laughin* i can’tttt omg 😂 u so dumb"),

("*slides into water* aaaaahhh this is heaven fr 💦", "*slips in beside him* mm yeahhh this hit diff 😩"),

("*leans on rock* yo i’m deadass never leavin this spot 😌", "*floats beside him* unless i pull u out for more kisses 😙"),

("*pulls her close* nevermind. i’m yours. drown me in love 😵‍💫", "*sits on his lap* challenge accepted 😚"),

("hinaaaa omg 😳 u bold bold today 😆", "*smirks* i’m just matching ur energy pervy prince 😝"),

("*wraps arms round her waist* u feel so damn good like this 😫", "*soft moan* narutooo... i swear this water ain’t the only thing steamin 🥵"),

("*leans close* lemme taste that cute mouth again 😘", "*kisses slow* mmm... keep goin... i’m not stoppin u 😩"),

("*deep kisses turnin heavy* yo this spring bout to explode from heat 😖", "*giggling breathless* stoppp u gon make me go feral 😵"),

("go feral baby... lose control... just with me 😏", "*moans soft* u got no idea what u do to me 😫"),

("*whispers in ear* u make me feel wild... like i ain’t ever felt love before 😮‍💨", "*smiles in neck* bc we real... raw... no masks out here ❤️"),

("god i wanna stay in this jungle forever... build a lil hut... make jungle babies 😳", "*blushing hard* narutoooo u did not just say that 😭"),

("i did 😤 jungle life > village life rn", "*laughing* u just want permanent hot spring access 😝"),

("nah... i want permanent u access 😏", "*kisses his jaw* then take me... always... anywhere 😚"),

("*lays back with her on chest* u feel that? my heart still racin 😬", "*presses ear to him* it’s sayin my name 🫠"),

("yo we need like a photo or sum... to remember all this 😩", "*smiling* nahh... let’s keep it sacred... just ours ❤️"),

("*nods* aight... memory sealed... like a scroll in my soul 😌", "*giggles* u n ur poetic jutsus 🙃"),

("yo lowkey the mist got my hair wild rn 😆", "*fixes it gently* u still cute... wild hair n all 😗"),

("*kisses her forehead* how’d i get so lucky 😔", "*whispers* bc u deserve love... all of it 💞"),

("*holds her tight in water* swear i’m never lettin this go... never lettin *you* go 🥺", "*leans into him* and i’ll never stop choosin u... over n over 😚"),

("*stepping out the hot spring* damn, the air feels so fresh after that 😌", "*wraps towel around* yeah, feels like we just hit reset or somethin 🫠"),

("yo, imagine us livin here one day, just chillin under the trees 🌳", "*smiles shy* that’d be like a dream... with u by my side 😚"),

("we’d wake up to birds singin, no alarms, no stress... just us 😍", "*nods* sounds perfect. i’d cook u breakfast every mornin 😝"),

("haha i’m down, but only if u promise to let me pick the playlist 🎶", "*laughs* deal! jungle jams only 😆"),

("*starts walking deeper into the jungle* this place is full of surprises huh", "*follows close* yeah, just like us 😌"),

("hey, remember when we got all muddy yesterday? i still can’t believe u slipped like that 😝", "*laughs* hey! that was a tactical fall, okay? totally planned 🙃"),

("sure sure... u just wanted an excuse to hold me close again 😉", "*grins* maybe... but can u blame me? u make it easy 😗"),

("true that... u got me wrapped around ur finger 🥹", "*whispers* and u love it too, admit it 😏"),

("fine, i do... u’re impossible to resist 😩", "*laughs* just wait till nightfall... i got more tricks up my sleeve 😈"),

("oh no... what kinda tricks we talkin bout here? 🙃", "*winks* you’ll see... jungle’s got its own magic when the stars come out 🌌"),

("ooh, sounds like a promise for another unforgettable night 😙", "*smiles* only the best for my queen 💞"),

("naruto... u always know how to make me feel special 🥺", "*pulls her close* that’s my job. making u feel loved every second 🫡"),

("well, u’re doing a damn good job 😌", "*kisses her softly* and it’s only just the beginning 😘"),

("*quiet moment* i love u, hina... more than words can say 🥹", "*smiles tearfully* i love u too, naruto... forever and always ❤️"),

("*night falls over jungle* stars twinklin bright above us 😮‍💨", "*looks up* it’s like the whole sky’s just for us huh 😌"),

("and here we are... alone, wild, free... just u and me ❤️", "*snuggles closer* feels like the world stopped just for this moment 😚"),

("yo hina... i gotta confess somethin", "*raises eyebrow* what’s up naruto? 🤨"),

("been thinkin bout this trip non-stop... how much u mean to me 🥹", "*heart skips* naruto... i feel the same. more than i ever thought possible 😍"),

("u make me wanna be better... stronger... for us", "*soft voice* and u inspire me to be brave... to love without fear 🥲"),

("*takes her hands gently* we’re like these trees... rooted strong, growin together even in wild storms 🌳", "*smiles* and no storm can break what we got 💞"),

("look at u... all brave and poetic n shit 😏", "*laughs* only when i’m with my queen 😉"),

("naruto... lemme tell u how much i love this trip, this jungle, but most of all... you 😚", "*eyes glisten* hina... u’re my light in every darkness, my calm in every chaos 🥺"),

("*leans in slow* i wanna make this night unforgettable... for us... forever 🥵", "*whispers* then show me... make me feel every bit of that love 😖"),

("*kisses deep, hands exploring gently* damn hina... u feel like fire and water all at once 🔥💦", "*moans soft* and u taste like every dream i ever had come true 😩"),

("i wanna hear u say my name... louder... like u mean it 😏", "*breathless* naruto... ugh... yes... keep goin..."),

("*their bodies move slow, perfectly synced, every touch a promise*", "*soft gasps and whispered names fill the cave*"),

("u always know how to make me lose myself... and i never wanna find the way back 🫠", "*smiles between kisses* that’s bc i’m home... when i’m with u 💞"),

("*hours pass like minutes, lost in their love and the jungle’s embrace*", "*holds her close, heart pounding* hina... u’re my forever adventure 🥹"),

("and u’re my forever home, naruto ❤️", "*they share a long, tender kiss*"),

("when this trip ends... we take this love with us. no matter where we go 🥲", "*nods* yeah... we build a life full of these moments. wild, messy, beautiful 😌"),

("promise me, we never stop exploring. not just the world... but each other 😗", "*smiling* promise. every day, every night, every breath 😚"),

("hey... next trip we bring the whole gang? imagine the chaos 😂", "*laughing* but we still steal our secret moments... just u and me 😘"),

("always... no matter how loud the world gets, u’ll be my quiet place 🥺", "*resting head on his chest* and u’ll be my strength when i’m weak 💞"),

("i love u naruto... more than i ever knew was possible 🥹", "*whispers back* i love u too, hina... more than words... more than time... forever 💖"),

("*morning light peeks through the trees* hey sleepyhead... u still wrapped up in dreams? 🥹", "*stretches* mmm only dream i want is u right here beside me 😗"),

("u smell like the jungle and a little bit like mischief too 😏", "*grins* gotta keep u on your toes babe 😉"),

("hope ur ready for another day of wild adventures... and maybe a lil trouble 😝", "*laughing* with u? always ready 🙃"),

("remember last night? i’m still buzzin from those kisses 😩", "*blushes* u made me forget the whole world... just me and u 😌"),

("i swear, u make the whole jungle feel like home 😮‍💨", "*softly* bc we’re building a home here... with every touch, every laugh 💞"),

("yo, what if we find a waterfall today? imagine us splashin and stealin kisses 😙", "*eyes sparkle* sounds perfect... u know how much i love those spontaneous moments 😘"),

("u always know how to make every second special... even in the middle of nowhere 😆", "*laughs* gotta keep the queen happy 😘"),

("hey, wanna race to that big tree over there? loser buys dinner 😉", "*smirks* you’re on! get ready to lose naruto 😝"),

("watch out! here i come! *runs like a wild kid* 😁", "*laughs and chases* no way u beating me today!"),

("*panting* okay okay... u win this round 😅", "*teasing* maybe i let u win... just a little 😉"),

("u sly... but i ain’t complainin 😆", "*wraps arm around her* gotta keep our love fun, right?"),

("always... u make everything better just by bein u 😚", "*smiles* and u make me wanna be my best self every day 🥹"),

("hey... can i tell u a secret? 🤭", "*curious* shoot"),

("sometimes i just stop and watch u... and i feel like the luckiest guy alive 😍", "*blushes* omg naruto... u make me melt"),

("no lie... u’re my whole world, hina ❤️", "*whispers* and u’re mine... forever and always 🥺"),

("so, waterfall next? or u got somethin else planned? 😉", "*grins* got a surprise... follow me 😏"),

("*leads her through the jungle, hand in hand* ready for this? 🥳", "*excited* always!"),

("*stops by a hidden clearing* tada! found a secret spot with the best view ever 😍", "*looks around* wow... this feels like our own little paradise 😌"),

("this is perfect... just like us 💞", "*pulls her close* and just wait... the best is yet to come 😘"),

("*sits down on a soft mossy rock* damn hina, this place got me feelin all calm n stuff 😌", "*leans head on his shoulder* me too... like time slowed just for us 🥹"),

("yo... u ever think bout how crazy it is? we started as just teammates and look at us now 😮", "*smiling* yeah, crazy how love sneaks up and grabs u tight without warnin 😗"),

("and here we are, lost in the jungle but foundin each other all over again 🥰", "*whispers* i never wanna lose u, naruto... not here, not ever 🥺"),

("got me thinkin... this jungle’s like a metaphor for us... wild, mysterious, full of surprises", "*nods* and sometimes a little scary but always worth the risk 💞"),

("i wanna keep explorin every inch of u... every secret, every dream 😌", "*grins* u always know the right things to say to get me soft and flustered 😝"),

("then get ready... bc i’m gonna make u feel things u never felt before 😏", "*biting lip* ohh naruto... u’re makin me hot just talkin bout it 😩"),

("got those eyes on me... like u wanna devour me whole 😮‍💨", "*leans in slow* maybe i do... wanna taste every inch, every sigh 😙"),

("u always so intense... and i love every second of it 🥵", "*laughs* good, bc i ain’t holdin back now"),

("*starts trailin kisses down her neck* how’s that feel? 😘", "*moans soft* like pure heaven... don’t stop 😖"),

("damn hina... u got me weak here 😫", "*whispers* good... i want u feelin every bit of this love 🥹"),

("imagine us makin love under the stars tonight... just u and me, no one else 💞", "*eyes sparkle* that sounds like a dream i never wanna wake from 😍"),

("u’re the only one i want, hina... no matter where this jungle takes us", "*smiling* and u’re the only one i trust with my heart 💖"),

("gonna hold u close all night long... keep u safe and warm 😌", "*wraps arms tighter* and i’ll be right here... never lettin go 😚"),

("u ready for more adventure tomorrow? jungle’s got a lot more to show us 😉", "*laughs* always ready with u by my side 😝"),

("let’s promise to keep making memories like this... wild, real, and full of love 🥰", "*nods* promise... forever and always 😘"),

("*morning dew on leaves* hey naruto, u think the jungle hears us laughin last night? 🤭", "*grinning* if it did, it probably wants in on the fun 😝"),

("u always know how to make me smile... even when we’re miles from the village 😌", "*softly* that’s bc u bring out the best in me, hina 💞"),

("yo, let’s find some wild fruit today... maybe share some juicy bites 😋", "*playful* only if u promise to share some kisses too 😘"),

("deal 😏", "*giggles* u’re impossible to resist when u smile like that 😗"),

("*picks a bright red berry* wanna try? they say it’s sweet and a lil spicy 😜", "*takes it* just like u, huh? 😉"),

("*laughing* exactly! wanna taste? *offers berry* 😆", "*bites slowly* mmm, wow... that’s good... like a secret jungle treasure 😮"),

("just like u hiding all those cute expressions 😙", "*blushes* stop ittt u gon make me shy again 😳"),

("nope... gotta keep u flustered, it’s part of my charm 😁", "*smiles* u got that down pat, naruto"),

("hey... wanna play a game? loser does a dare 😈", "*curious* ooo i’m in... what’s the game?"),

("truth or dare... jungle edition 😏", "*laughs* u sure wanna risk that?"),

("always... bring it on, hina 😝", "*smirks* okay... truth or dare?"),

("truth 😌", "*serious* what’s the most embarrassing thing u ever did for me?"),

("hmm... probably when i tried to cook u dinner and almost burned the whole camp 😂", "*laughs* omg i forgot that! u were a disaster in the kitchen 😆"),

("hey! i was tryin my best... but u still ate it all and said it was the best meal ever 😘", "*smiling* bc u made it with love... and that’s what counts 💞"),

("okay my turn... truth or dare? 😉", "*thinking* dare! i’m fearless after last night 😈"),

("i dare u to kiss me right here, right now 😏", "*leans in* say no more 😘"),

("*their lips meet, soft then deepening* u always win the dares, huh? 😩", "*giggles* bc u make them impossible to refuse 😚"),

("this jungle’s got magic... or maybe it’s just us 💕", "*smiling* either way, i never wanna leave this spellbound feeling 🥲"),
("*walking along a narrow path* yo hina, you think this jungle’s got hidden treasure? 🤨", "*grinning* maybe... but I think I already found mine 😉"),

("aww, smooth talker! you always got those cheesy lines ready huh 😆", "*laughs* can’t help it when I’m with you 😌"),

("hey, wanna see who can climb that big tree faster? loser owes the winner a kiss 😏", "*smirks* challenge accepted, but don’t cry when you lose 😝"),

("*starts climbing* bet you didn’t see me this fast before! 🫡", "*laughs* ugh, no way you’re beating me! *climbs fast*"),

("*reaches top first* haha! you’re slow today, ninja! 😜", "*panting* no fair! you cheated somehow! 😒"),

("cheated? pfft, I’m just naturally awesome 😁", "*rolls eyes* yeah yeah, Mr. Hokage"),

("hey, wanna see a secret spot I found yesterday? promise it’s worth it 😘", "*intrigued* ooh, lead the way!"),

("*takes her hand and leads through thick bushes* almost there... just a little more 😌", "*whispers* naruto, it’s beautiful here... wow 😍"),

("thought you’d like it... nature’s own little hideaway for us 💞", "*leans on his shoulder* feels like our secret world, away from everything"),

("you know, being here with you makes me forget all the crazy ninja stuff for a bit 😌", "*smiles* me too... just us, the jungle, and the stars coming soon 😏"),

("hey... remember that time you tried to flirt and almost tripped? I swear, you’re a mess sometimes 😝", "*laughs* hey, gotta keep things interesting!"),

("and you definitely do... in the best way possible 😘", "*blushes* stoppp you’re making me shy!"),

("nah, just telling the truth. you’re adorable when you’re flustered 🥰", "*giggles* well, you’re just lucky I’m crazy about you 😚"),

("crazy about you too, hina. Every single day 🥹", "*resting her head on his chest* that means everything to me 🥲"),

("let’s stay here a while... just us, no worries, no plans, just love ❤️", "*nods* I’m all in, naruto, forever and always"),

("*the sun starts to set, painting the sky orange* hey hina, look at that sky... kinda like your smile, yeah? 😉", "*blushes* stop it, naruto, you’re making me melt here 😳"),

("good, that’s the plan 😏 wanna sit here and watch the stars come out with me? 😌", "*nods* nothing sounds better than that... just you and me, no distractions 😚"),

("you always know how to make ordinary moments feel special 🥲", "*softly* bc with you, everything’s special 💞"),

("*pulls her close* hey... you ever think about what comes after this trip? what life looks like? 🤨", "*smiles shy* sometimes... as long as you’re in it, I’m ready for anything 🥰"),

("yeah... me too. I wanna build something real with you, hina. Not just dreams but real life 🥺", "*eyes shine* you’re my forever, naruto. I’m ready to take that step with you ❤️"),

("promise me one thing? no matter what happens, we keep loving like this—wild, honest, and real 💞", "*holds his hand tight* promise. No games, no masks, just us 🥹"),

("you’re incredible, hina... more than I ever thought I deserved 😌", "*smiles* and you’re my hero. Always have been, always will be 🥰"),

("hey... wanna make a memory? right here, right now. Something we’ll never forget 😏", "*raises eyebrow* I’m curious... what do you have in mind?"),

("*grins* close your eyes", "*closes eyes* okay..."),

("*soft lips brush hers* this kiss is for every time we laughed, every time we held on, every time we dreamed together 😘", "*moans softly* naruto... you’re everything to me 😩"),

("got more where that came from... wanna take this night slow, feel every moment? 🥵", "*whispers* yes... make me feel alive, like only you can 😖"),

("*hands tracing her curves gently* hina, you’re fire and calm all at once 🔥💦", "*breathless* and you’re the only one who knows how to handle both sides 😚"),

("let’s make this night ours, no rush, no worries... just love and us ❤️", "*nestles closer* I’m yours, naruto. Always and forever 🥲"),

("*moonlight filtering through leaves* hey hina, feel that? jungle’s alive tonight... just like us 😏", "*smiling* yeah... it’s like the whole world’s watching our story unfold 🥰"),

("you know, sometimes i get nervous... but then i look at u and feel brave again 🥺", "*touches his cheek* naruto, u don’t have to be strong all the time. i’m here. always 💞"),

("i like that... us being strong together. makes me wanna love u even more 😌", "*giggles* u always say the sweetest things... got me blushing like crazy 😝"),

("hey, wanna play a little game? jungle style 😏", "*curious* what kinda game?"),

("truth or dare... with a twist. loser gets a kiss... and maybe a lil more 😉", "*laughs* u’re on, but u better watch out"),

("truth for me! ready? ask away 😁", "*smirks* what’s the naughtiest thought u had about me since we got here?"),

("*laughs nervously* omg naruto, u’re wild! okay, i gotta admit... thought about u and me alone by that waterfall... u know... getting a little crazy 😖", "*grins* ohh, that’s hot... gotta say i been thinkin the same"),

("alright, my turn... dare!", "*raises eyebrow* i dare u to whisper the dirtiest thing u wanna do to me right now 😈"),

("*blushes deeply* hmm... i wanna feel u close, hands everywhere, making u mine till u can’t breathe 😩", "*moans softly* hina... u got me speechless 😵‍💫"),

("now your turn, truth or dare? 😉", "*breathless* dare... i’m fearless with u 😏"),

("i dare u to kiss me like it’s the last time on earth 😘", "*leans in slowly* then i won’t hold back 😗"),

("*their lips meet, hungry and sweet, tongues dancing* u make me crazy, naruto", "*whispers* u’re my addiction, hina"),

("let’s not stop... wanna feel every second of this night with u 🥵", "*nuzzles neck* take me there... please 😖"),

("we’re wild and free... jungle’s magic or maybe just us? 🤭", "*smiles* either way, i never wanna lose this feeling 💞"),

("*soft breeze rustling leaves* hina, you know what? every time you smile, my heart does this crazy flip 😩", "*giggles* u’re such a sap, naruto... but i love it 🥰"),

("i can’t help it... u make me feel things no one else ever could 💞", "*rests head on his chest* and u make me feel safe, like nothing bad can touch me here 🥲"),

("hey, wanna explore that cave we saw earlier? might be dark... but i think we’ll light it up 😏", "*eyes sparkle* with u? i’m ready for any adventure"),

("watch ur step tho... jungle’s full of surprises, like me getting lost in ur eyes 😘", "*laughs* stoppppp, u’re killin me here 😳"),

("oh no, mission ‘make hina blush’ is working 😆", "*smiles shy* well, ur doing a great job"),

("remember when we first met? never thought this would be us... wild jungle, crazy love, all in one 🥲", "*softly* yeah... it’s been one hell of a journey... and i wouldn’t change a thing"),

("wanna make a pact? no matter what comes next, we face it together. jungle or not ❤️", "*nods* forever and always, naruto. you and me against the world 🥹"),

("hey, can i be honest? sometimes i get scared... scared of losing u", "*holds her hand* i’m right here, hina. never letting go, no matter what 😌"),

("that means everything to me... you’re my rock, my light 💞", "*smiling* and u’re mine... the fire that keeps me warm in this jungle"),

("so... what’s the craziest thing u wanna do with me before this trip ends? 😏", "*grins* gotta say, i wanna steal as many kisses as i can, especially the naughty ones 😝"),

("oh, u’re on! better be ready for me, hina", "*laughs* bring it, naruto. i’m not backing down 😘"),

("how about a midnight swim under the stars? just u, me, and the water", "*eyes wide* omg yes! that sounds perfect 😍"),

("then it’s settled. we make memories we’ll never forget 💦", "*nods* with u, every moment is unforgettable 🥲"),

("*stars twinkling above* hina, you ready for that swim? water’s perfect and so am i when i’m with u 😏", "*smiles* always ready when u ask so sweetly 😘"),

("c’mon, let’s ditch the clothes and just be us, wild and free 🥵", "*laughs* you’re so bold... but i’m down 😗"),

("*both step into the cool water, splashing playfully* hey, don’t splash me too hard! 😆", "*grins* gotta keep u on your toes, princess 😉"),

("u’re impossible... and i love it 😚", "*laughs* right back at ya, naruto"),

("underneath the stars, water shimmering... feels like a dream i never wanna wake from 🥰", "*softly* u make everything magical, hina"),

("*pulls her close* wanna make this moment last forever? 💞", "*nods* hold me tight, naruto, don’t ever let go 🥲"),

("can’t help myself... gotta taste u here, now 😘", "*moans softly* please, don’t stop"),

("u’re like fire in the water... so hot and cool at the same time 🔥💦", "*giggles* only you understand me like that 😝"),

("hey, remember that time we got caught in the rain? felt like the whole jungle was cheering for us 😁", "*smiling* yeah, best day ever. rain or shine, we’re unstoppable together"),

("let’s make a promise... no matter where life takes us, we keep that wild spark alive ❤️", "*squeezes his hand* promise, naruto. forever wild, forever us 🥹"),

("can’t wait to see what other adventures we find... and maybe a few more kisses too 😏", "*winks* oh, there’ll be plenty... trust me 😘"),

("u drive me crazy, naruto... in the best way 😩", "*laughs* that’s my job, hina"),

("let’s swim a little deeper... find a spot just for us 💦", "*nervous but excited* lead the way, i’m all in 😍"),

("*slowly swimming deeper into the water* hina, u feel that? like the jungle’s breathing with us 🥵", "*whispers* yeah... like it’s alive with our energy, naruto 😌"),

("i never thought being lost in the jungle could feel so right... when i’m with u 🥲", "*smiling* me too. it’s like every step we take, we’re writing our own story 💞"),

("hey... wanna try something wild? let’s find a hidden waterfall and just get soaked in love 😏", "*eyes sparkling* u’re always full of surprises... i’m in 😘"),

("imagine the water rushing over us... us holding each other tight, lost in the moment 💦", "*blushes* u make me feel so alive, naruto... like nothing else matters"),

("your hands on me... warm and steady... like the jungle’s heartbeat matching mine 🥰", "*leans closer* every touch feels electric... i’m yours, hina, completely 😩"),

("sometimes i can’t believe how lucky i am to have u... in this crazy wild world 🌎", "*softly* i’m the lucky one... u make me stronger and softer all at once 🥹"),

("okay, i gotta confess... i’ve been thinking about u all day. those lips, that smile, everything 😝", "*laughs* naruto, u’re hopeless... but i love it"),

("u make my heart race... and sometimes i just wanna throw all the rules away and be crazy with u 😘", "*biting lip* same here... let’s get lost in this moment, no holding back 😏"),

("u know, the jungle’s got us surrounded, but with u, i feel like we’re the only two people in the world 🥺", "*wraps arms around her* that’s bc we are, hina. just u and me, forever 💞"),

("hey... wanna play a game? jungle truth or dare, but with no secrets kept 😉", "*smirks* u’re on, but be ready for the heat i’m bringing 😈"),

("truth first! what’s the wildest thing u wanna do with me right here, right now? 😮", "*whispers* i wanna kiss u till we forget where we are, then take u slow, feel u close, real close 😖"),

("damn, hina... u don’t hold back. i love that fire in u 🔥", "*smiling* it’s only for u, naruto"),

("okay, dare time! i dare u to tell me the dirtiest thought u’ve had about me since we started this trip 😝", "*laughs* alright, here goes... i keep imagining u biting that lip of yours while i trace my fingers down ur back... until u shiver under me 😩"),

("shit, u got me speechless... and kinda hot just thinkin bout it 😳", "*teasing* just wait, there’s more where that came from"),

("truth or dare, naruto? ready to lose? 😏", "*grins* bring it on, i’m fearless with u"),

("dare! i dare u to kiss me like it’s the last time u’ll ever get to taste me 😘", "*leans in slow and deep* then i’m never letting go 😗"),

("*kisses deep, hands roaming, breaths mingling* u drive me crazy, hina... my heart’s on fire 🥵", "*moans softly* take me there, naruto, i’m yours"),

("let’s get outta the water and find a soft spot under the trees... where i can hold u close and never let go 💞", "*nods* sounds perfect. just u, me, and the jungle’s symphony"),

("*lying down on the mossy ground* u’re so warm, naruto... makes me wanna melt right here 😍", "*brushes hair from her face* u’re beautiful, hina. inside and out 🥲"),

("i wanna memorize every inch of u... every smile, every touch, every sigh 😌", "*smiling* and i wanna feel ur love in every heartbeat"),

("hey... wanna hear a secret? i get weak in the knees just hearing u say my name 😝", "*laughs* hina... u got me blushing real hard now 😳"),

("u got me feelin like the luckiest man alive... and i’ll prove it to u every day 💖", "*softly* i believe that, naruto. i trust u with my heart 🥹"),

("let’s promise to keep this fire burning... wild, raw, and real no matter what comes next 🔥", "*holds his hand tight* promise. u and me, forever and always ❤️"),

("hey... wanna fall asleep wrapped in each other? no jungle noises, just us 🥰", "*smiles* that’s the best dream i ever had"),

("*whispers* naruto, u’re my home... my heart’s safe with u 🥲", "*holds her close* and u’re mine, hina. always"),

("*early morning jungle mist surrounds them* hina, waking up next to you feels like a dream i never wanna wake from 😌", "*smiles softly* same here, naruto... your warmth is my favorite kind of sunshine ☀️"),

("i swear, every little thing u do... from the way u laugh to how u look at me... it’s magic 💞", "*blushes* u always know how to make me feel special. like the only girl in the world 🥹"),

("hey, wanna sneak away today? just the two of us... explore deeper parts of the jungle? 😏", "*eyes sparkle* oh yes, let’s make some unforgettable memories 😘"),

("i love how wild and free u make me feel... like we can forget everything else for a while 🥵", "*giggles* that’s the plan. jungle adventures with a side of mischief 😉"),

("u think there’s a hidden spot where no one else has been? maybe a secret pool or waterfall? 🤨", "*nods* i heard stories from the locals... if we find it, it’s gonna be ours alone 💦"),

("sounds perfect... and i’m already imagining us there... just u and me, no distractions 😘", "*biting lip* u know i’m ready to make those dreams real 😩"),

("hey, wanna race? first one to that big tree by the river gets to choose what happens next 😏", "*laughs* you’re on, naruto. prepare to lose 😝"),

("*both sprint through thick foliage, laughing and dodging branches* this is way too much fun! 😆", "*panting* okay, okay, you win! but only ’cause i let u 😉"),

("oh really? i think u just wanted an excuse to see me all sweaty and wild 😜", "*blushes* maybe... but u don’t mind, do u?"),

("never. u look amazing like this. makes me wanna kiss u right here 😘", "*eyes wide* now that’s an offer i can’t refuse 😗"),

("*their lips meet in a messy, passionate kiss* u’re driving me crazy, naruto 🥵", "*smiles against her lips* that’s the plan, hina"),

("hey... u ever think about us, like really think? where we’ll be in a few years? 🥺", "*softly* all i know is i want u there with me. no matter what happens, we face it together ❤️"),

("promise me something? no matter what, we keep being this real, this honest, this crazy about each other 💞", "*nods* promise. u’re my forever, naruto 🥲"),

("i love u, hina. more than words could ever say 🥹", "*tears in eyes* i love u too, naruto. always have, always will 🥰"),

("hey, wanna rest here a bit? just breathe and feel the jungle around us 🌿", "*leans her head on his shoulder* sounds perfect. u make me feel so safe"),

("and u make me feel alive. like i can take on anything, as long as u’re by my side 😌", "*smiles* together, we’re unstoppable"),

("okay, one last game? truth or dare... jungle edition 😈", "*grins* bring it on, naruto"),

("truth! what’s the craziest thing u wanna do with me before we leave this jungle? 😏", "*whispers* i wanna lose myself in u... kiss u till we’re breathless, touch u till we forget the world 😩"),

("damn hina... u got me all fired up just thinking about it 😳", "*laughs* u’re impossible"),

("dare! i dare u to show me how much u want me, right here, right now 😘", "*pulls her close, voice low* then i’m gonna make u feel it in every kiss, every touch, every breath we share 😗"),

("*they fall into each other, jungle sounds fading away as their world shrinks to just the two of them* u’re my everything, hina 🥵", "*softly* and u’re mine, naruto. forever and always 💞"),

]

story_index = 0

async def detect_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global group_chat_id, chat_started
    if group_chat_id is None and update.effective_chat.type in ["group", "supergroup"]:
        group_chat_id = update.effective_chat.id
        logging.info(f"Detected group chat ID: {group_chat_id}")
        await context.bot.send_message(chat_id=group_chat_id, text="A Romantic Jungle Tour Of Naruto And Hinata 💞")
        chat_started = True

async def chat_loop(bot1, bot2):
    global story_index
    while not chat_started:
        await asyncio.sleep(1)

    await asyncio.sleep(2)

    while True:
        if story_index >= len(story_sequence):
            story_index = 0

        naruto_line, sakura_line = story_sequence[story_index]

        await bot1.send_chat_action(chat_id=group_chat_id, action="typing")
        await asyncio.sleep(2)
        await bot1.send_message(chat_id=group_chat_id, text=naruto_line)

        await asyncio.sleep(5)

        await bot2.send_chat_action(chat_id=group_chat_id, action="typing")
        await asyncio.sleep(2)
        await bot2.send_message(chat_id=group_chat_id, text=sakura_line)

        story_index += 1
        await asyncio.sleep(6)

async def main():
    app1 = ApplicationBuilder().token(BOT1_TOKEN).build()
    app2 = ApplicationBuilder().token(BOT2_TOKEN).build()

    app1.add_handler(MessageHandler(filters.ALL, detect_chat))
    app2.add_handler(MessageHandler(filters.ALL, detect_chat))

    await app1.initialize()
    await app2.initialize()
    await app1.start()
    await app2.start()

    logging.info("Bots are ready. Add them to a group and send any message to start.")

    await asyncio.gather(
        app1.updater.start_polling(),
        app2.updater.start_polling(),
        chat_loop(app1.bot, app2.bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
