-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 17, 2022 at 08:19 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- START TRANSACTION;
-- SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_tags`
--

-- --------------------------------------------------------

--
-- Table structure for table `quotes`
--

DROP TABLE IF EXISTS `quotes`;
CREATE TABLE IF NOT EXISTS `quotes` (
  `ID` varchar(500) NOT NULL,
  `LINE` longtext NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `quotes`
--

INSERT INTO `quotes` (`ID`, `LINE`) VALUES
('1', '```If there aren\'t any books, I\'ll just have to make them myself.``` — Myne, Part 1 Volume 1 Chapter 5'),
('2', '```I will never give up, no matter what. Forget all that about me being a normal girl. I\'m going to become the weirdest, strangest girl who ever lived!``` — Rozemyne to Ferdinand in Part 3 Volume 3 Chapter 5: A Class for Kids'),
('3', '```I only start fights that I know I can win.``` — Ferdinand to Myne in Part 2 Volume 2 Chapter 24: The Healing Ritual'),
('4', '```Cause you made my dream come true, and now I want to return the favor. I\'ll make a ton of books for you and send them your way, so don\'t cry.``` — Lutz in Part 4 Volume 3, Chapter 19: A Promise'),
('5', '```When you get the chance to earn money, take it and profit as much as you possibly can.``` — Benno to Myne in Part 1 Volume 2, Chapter 13: The Guildmaster\'s Granddaughter'),
('6', '```No sound is more pleasant to the ears than that of coins rubbing together, don\'t you agree?``` — Freida to Myne in Part 1 Volume 2, Chapter 13: The Guildmaster\'s Granddaughter'),
('7', '```You\'re an angel, Tuuli. The healer of my heart. You\'re the greatest older sister in the world.``` — Myne to Tuuli in Part 1 Volume 2, Chapter 14: Freida\'s Hair Ornaments'),
('8', '```She has the loyalty to wield a blade against me without hesitation, but she is shockingly brainless.``` — Ferdinand remarking on Angelica to Rozemyne in Part 4 Volume 3, Chapter 1: The Dedication Ritual and Returning to the Castle'),
('9', '```I wish for everyone to consider you as much of a saint as I do, and to that end, I will spare no expense.``` — Hartmut to Rozemyne in Part 4 Volume 1 Chapter 10: Royalty and Nobles from Other Duchies'),
('10', '```Even when a woman asks your opinion, know that her heart is already set on something. She simply wants you to agree with her, so she will only be disappointed if you pick or compliment something other than her preference.``` — Veronica\'s advice to her grandson Wilfried, Royal Academy Stories - First Year'),
('11', '```I\'ll take good care of you as my little sister. All I ask, Rozemyne, is that you take good care of Lord Ferdinand too.``` — Eckhart to Rozemyne in Part 3 Volume 1 Chapter 3: A Noble\'s Baptism Ceremony'),
('12', '```Myne, this man has a terrible personality. But he has something of a good heart underneath his rotten everything else.``` — Ferdinand remarking on Sylvester to Myne in Part 2 Volume 3, Chapter 13: Preparing for the Spring Prayer'),
('13', '```As always, Justus frames everything to be in his favor. Rozemyne, know that he is an eccentric man. He loves gathering information and materials above all else.``` — Ferdinand to Rozemyne in Part 3 Volume 2, Chapter 10: Preparing for the Harvest Festival'),
('14', '```Yes, she\'s my little sister. She\'s very competent, unlike me, so our parents compliment her all the time.``` — Angelica describing Lieseleta to Rozemyne in Part 4 Volume 1, Chapter 7: My Retainers and Entering the Dormitory'),
('15', '```Are you the fool who kidnapped my only granddaughter?!``` — Bonifatius in Part 3 Volume 5, Chapter 13: Rescue'),
('16', '```Lady Florencia is two years older than Lord Sylvester, and has the incredible power of being able to control her husband.``` — Karstedt to Rozemyne in Part 3 Volume 1, Chapter 4: Adoption'),
('17', '```I\'ll do my best not to waste the opportunity given to me. Thank you, Ferd — No, thank you, Uncle.``` — Wilfried to Ferdinand in Part 3 Volume 5, Chapter 9: Wilfried\'s Punishment'),
('18', '```I have resolved to make books with you, Lady Rozemyne. I will not turn my back on that decision.``` — Philine in Part 4 Volume 3, Chapter 8: A Week of Socializing'),
('19', '```Roderick was among those who tricked Lord Wilfried, so he is by no means fit to serve you, milady.``` — Rihyarda to Rozemyne in Part 4 Volume 1, Chapter 7: My Retainers and Entering the Dormitory'),
('20', '```My family\'s bottom of the barrel even among laynobles, and my whole life I\'ve been walked over by people of higher status than me. Almost nobody\'s ever stuck their neck out and helped me before.``` — Damuel to Rozemyne in Part 2 Volume 3 Chapter 6: Punishment for the Knight\'s Order and My Future'),
('21', '```In order for Ehrenfest to move on to the next stage of strength, it is necessary for all of our apprentice knights to face their limits.``` — Leonore to Rauffen in Part 4 Volume 2, Life without One\'s Lady'),
('22', '```Come to me whenever you like. I\'ll destroy any villain who makes my adoptive daughter cry.``` — Karstedt to Myne in Part 2 Volume 3, Chapter 13: Spring Prayer'),
('23', '```Y\'know, I don\'t think you have much to worry about. I know I\'ll be proud to have you as my little sister.``` — Cornelius to Rozemyne in Part 3 Volume 1, Being My Little Sister\'s Knight'),
('24', '```I\'d tutored Lord Karstedt since he was a little boy, and then I was Lord Sylvester\'s wet nurse … I\'ve known Lord Ferdinand since he was a young boy too, going all the way back to when he was first brought to the castle.``` — Rihyarda to Rozemyne in Part 3 Volume 1, Chapter 9: The Archduke\'s Castle'),
('25', '```I would like for Ehrenfest fashion to dominate for at least a brief period while I am attending the Royal Academy.``` — Brunhilde to Rozemyne in Part 4 Volume 1 Chapter 7: My Retainers and Entering the Dormitory'),
('26', '```I wish to see no more battles for power and authority, yet my decision here may create another tragedy like the one that took my family. I do not want to plant the seeds of war.``` — Eglantine to Rozemyne in Part 4 Volume 2, Chapter 13: A Tea Party with Eglantine'),
('27', '```I… wanted to ask if we could possibly be friends…?``` — Hannelore to Rozemyne in Part 4 Volume 3, Chapter 11: The Tea Party for All Duchies'),
('28', '```My apologies, but I see I must make this clear — you and I are not cousins.``` — Detlinde to Rozemyne in Part 4 Volume 1 Chapter 20: Dedication Whirl'),
('29', '```The person Georgine hates and resents above all else is Sylvester — the one who stole the position of aub from her.``` — Ferdinand to Rozemyne in Part 3 Volume 4, Chapter 18: Dirk\'s Mana and Submission Contract'),
('30', '```Lady Rozemyne does not require such fanatic loyalty in the least, nor does she understand the value of receiving a name, She also values the free will of others to such an extent that she allows even gray priests and shrine maidens to make their own decisions. It is hard to imagine that she would appreciate a display that stands for the complete opposite.``` — Hartmut to Rozemyne\'s retainers in Part 4 Volume 5: Hirschur\'s Visit and the Advancement Ceremony'),
('31', '```You idiot! Think for just one second before you pull this garbage, come on!``` — Benno to Myne in Part 1 Volume 3: Benno\'s Lecture'),
('32', '```No, Dad, you\'ve protected me my whole life. If I ever get married, I hope it\'ll be to someone strong who can protect me just like you have.``` — Myne to her dad in Part 2 Volume 4: Ripped Apart'),
('34', '```I do not know how, but Lady Rozemyne is now the active master of Schwartz and Weiss, the library\'s magic tools. It seems to be the work of the gods``` — Hirchur\'s report to Sylvester in Part 4 Volume 1: Epilogue'),
('33', '```O mighty King and Queen of the endless skies, ye mighty God of Darkness and Goddess of Light; O mighty Eternal Five who rule the mortal realm, ye mighty Goddess of Water Flutrane, God of Fire Leidenschaft, Goddess of Wind Schutzaria, Goddess of Earth Geduldh, God of Life Ewigeliebe; I ask that ye hear my prayers and grant thy blessings. I offer thee my heart, my prayers, my gratitude, and ask for thy holy protection. Grant those I love the power to strive toward their goals, the power to deflect malice, the power to heal their pain, and the power to endure trials and tribulations.``` — Myne\'s final blessing to her famiily in Part 2 Volume 4: Ripped Apart'),
('35', '```Is it not blindingly obvious that this is what happens when one foolishly puts other people between Rozemyne and the library? Understand that I proposed forbidding her from entering the library until she passed all her classes to ensure she would be finished in time for the Dedication Ritual. Wilfried was a fool for not realizing this and stupidly adding on the condition that all the other first-years had to pass their classes as well, and to be clear, it is not easy to control Rozemyne. Recall that, despite entering the temple for the first time at her baptism, she charged blindly ahead to Bezewanst and offered an entire large gold for him to take her as a shrine maiden, all so that she could enter the temple book room. With the Royal Academy\'s library now within reach, there is obviously nothing that could stop her.``` — Ferdinand to Sylvester in Part 4 Volume 1: Epilogue'),
('36', '```This is all about Rozemyne! What\'s that little gremlin doing over there?!``` — Sylvester\'s thoughts on Rozemyne in Part 4 Volume 1: Epilogue'),
('37', '```Thank you ever so much, Professor Solange. I am truly, truly glad—beyond words, even—to have been blessed with entering this paradise given to us by the gods. Let us pray to Mestionora the Goddess of Wisdom in thanks for this meeting with the Royal Academy! Praise be to the gods!``` — Rozemyne\'s blessing in the library in Part 4 Volume 1: Registering at the Library'),
('38', '```The library is replete with the precious gems of knowledge given to us by Mestionora the Goddess of Wisdom. Only those who swear by her name that they will treat its books with care are allowed inside.``` — Solange to Rozemyne in Part 4 Volume 1: Registering at the Library'),
('39', '```O Goddess of Water Flutrane, bringer of healing and change, O twelve goddesses who serve by her side. Please hear my prayer and lend me your divine strength. Grant me the power to heal your sister, the Goddess of the Earth Geduldh, who has been wounded by those who serve evil. I pray that holy music be granted, casting ripples of the highest order. May I be filled with the royal color to mine own heart\'s content.``` — Rozemyne healing the earth in Part 2 Volume 2: Healing Ritual'),
('40', '```You sound entirely like a jealous wife...``` — Hartmut to Rozemyne in Part 4 Volume 6: Roderick\'s Wish'),
('41', '```I do not intend to give my name to anyone, I wish to make my own decisions, and decide my own path through life. One can surely count the number of name-sworn nobles on one hand, and I believe that loyalty can be given even without making such a sacrifice.``` — Brunhilde to Rozemyne in Part 4 Volume 5: Hirschur\'s Visit and the Advancement Ceremony'),
('42', '```I feel that name-swearing is best done not to show one\'s loyalty, but to express love to another—to give one\'s name to one\'s dearest and receive theirs in turn, thereby forming an eternal vow of everlasting love. However, that is hardly realistic. I do not believe it will ever happen for me.``` — Leonore to Rozemyne in Part 4 Volume 5: Hirschur\'s Visit and the Advancement Ceremony'),
('43', '```I saw with my own eyes the joy our brother Eckhart felt when he earned Lord Ferdinand\'s trust through giving his name, and the despair he felt when he sheltered in the temple, I don\'t think I could give my name to someone after seeing how low he was.``` — Cornelius to Rozemyne in Part 4 Volume 5: Hirschur\'s Visit and the Advancement Ceremony'),
('44', '```Nooo! At this rate, I won\'t even be as hard-boiled as an egg! I\'m just a soft, squishy soft-boiled one!``` — Rozemyne\'s thoughts on her water gun in Part 4 Volume 6: Strengthening the Weapon'),
('45', '```I see the divine instruments are very pretty...``` — Hildebrand to Rozemyne in Part 4 Volume 7: The Ternisbefallen Inquiry'),
('46', '```I\'m sorry! So sorry! I might have just made a really serious mistake! It\'s not my fault, though! I\'ve said from the beginning that we used the God of Darkness\'s blessing, so I couldn\'t lie about where I read the prayer! And our bible certainly isn\'t the inaccurate one here!``` — Rozemyne\'s thoughts to herself during the inquiry in Part 4 Volume 7: The Ternisbefallen Inquiry');

-- --------------------------------------------------------

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
CREATE TABLE IF NOT EXISTS `tags` (
  `NAME` varchar(500) NOT NULL,
  `LINK` varchar(500) NOT NULL,
  `ID` varchar(255) NOT NULL,
  PRIMARY KEY (`NAME`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tags`
--

INSERT INTO `tags` (`NAME`, `LINK`, `ID`) VALUES
('CD1Latest', 'https://cdn.discordapp.com/attachments/1023390923511562361/1024819810393137193/CD1BookWorm.m4b.vtt', '544655732142768151'),
('Myne', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028463905569243166/unknown.png', '519916455857487872'),
('Lutz2', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028483672799723611/unknown.png', '519916455857487872'),
('praisebetothegod', '<:praisekami:946117405111898192>', '519916455857487872'),
('Ferdinand', 'https://cdn.discordapp.com/attachments/901265330830213180/1028484509269774466/Ferdinand-LN-1_2.jpg', '519916455857487872'),
('Freida', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/a/a6/Freida-LN-1.jpeg/revision/latest?cb=20211213172053', '519916455857487872'),
('Mestionora', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/9/9e/Mestionora.png/revision/latest?cb=20221004234442', '519916455857487872'),
('DramaCd2', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/9/9c/Ascendance_of_a_Bookworm_Drama_CD_2.jpg/revision/latest?cb=20190903144217', '519916455857487872'),
('ChibiFerdie', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/9/9b/Manga_P2V1-BackCoverJPN.jpg/revision/latest?cb=20201116115044', '519916455857487872'),
('Storytime', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/b/bd/LN_P1V3-5.jpg/revision/latest?cb=20210418183055', '519916455857487872'),
('Hartmut', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028494808785899591/unknown.png', '519916455857487872'),
('Lieseleta', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/f/f0/Lieseleta-LN.jpg/revision/latest?cb=20211213134431', '519916455857487872'),
('Lutz3', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028536415379796018/unknown.png', '519916455857487872'),
('WeirdJustus', 'https://static.wikia.nocookie.net/ascendance-of-a-bookworm/images/a/a9/Justus-Anime-2.jpg/revision/latest?cb=20210505000650', '519916455857487872'),
('Lutz', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028480322112868453/unknown.png', '519916455857487872'),
('Mesti', 'https://cdn.discordapp.com/attachments/1023753007671824487/1028559393945554984/Mestionora_FB3.png', '519916455857487872'),
('Geduldh', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028675268887462009/unknown.png', '519916455857487872'),
('chibiflan', 'https://cdn.discordapp.com/attachments/1023753007671824487/1028678927780155472/FILE-26.png', '519916455857487872'),
('Angelica', 'https://cdn.discordapp.com/attachments/1023753007671824487/1028682996137603172/20220930_194249.jpg', '519916455857487872'),
('Flutrane', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028707992792727662/unknown.png', '519916455857487872'),
('Leidenschaft', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028853124980551720/unknown.png', '519916455857487872'),
('Schutzaria', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028853290387132416/unknown.png', '519916455857487872'),
('Ewigeliebe', 'https://cdn.discordapp.com/attachments/1027597999091753010/1028853434612449402/unknown.png', '519916455857487872'),
('RozemynePen', 'https://cdn.discordapp.com/attachments/1023753007671824487/1028913065447661618/R_FILE-13.png', '544655732142768151'),
('PraiseRozemyne', 'https://media.discordapp.net/attachments/1023753007671824487/1028915677597278298/LN_P4V9-2.jpg', '468575639075553311'),
('MyneDance', 'https://tenor.com/view/ascendance-of-a-bookworm-dancing-swing-happy-joy-gif-17651414', '468575639075553311'),
('BezeCrush', 'https://media.discordapp.net/attachments/1023753007671824487/1028924072639340626/LN_P1V3-6_1.jpg', '468575639075553311'),
('cursedbook', 'https://cdn.discordapp.com/attachments/946041447348596747/1029885170427375647/bookworm.webm', '519916455857487872'),
('PockyTag', 'Pocky :D', '468575639075553311'),
('goodtimes', 'https://media.discordapp.net/attachments/837289343969132575/955740152930656256/c4pwyr.gif', '519916455857487872');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
