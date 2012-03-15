$(function() // execute once the DOM has loaded
{
  $("#answerForm").submit(function(event)
  {
    event.preventDefault();
    checkAnswer();
  });

  $("#answerbox").keyup(function(event)
  {
    if (event.keyCode == 27 /*esc*/) 
	$("#answerbox").get(0).value = "";
  });

  $("#answerbox").get(0).focus();
});

var lastAnswer = "";
function checkAnswer() {
	var answer = $("#answerbox").val();
	if (answer == lastAnswer) return false;
	else lastAnswer = answer;
	result = decode(encodedClue, encodedClueChecksum, answer);
	if (result != "")
		showNext(result);
	else 
		showError(answer, randomError());
	
	return false;
}

var fadeout;
function stopAnim() {
	clearTimeout(fadeout);
	$("#wrongdiv").stop(true,true);
}

function showNext(strResult) {
	$("#resultlink").get(0).innerHTML = resultLinkAnchor.replace("%s", strResult);
	$("#resultdiv").slideDown(5000);	
}

function showError(answer, errorText) {
	console.log("Incorrect answer: " + answer);
	$("#resultdiv").stop().hide();
	var wrongdiv = $("#wrongdiv");
	stopAnim();
	$("#wrongtext").get(0).innerHTML = errorText;
	wrongdiv.fadeIn();
	fadeout = setTimeout("$(\"#wrongdiv\").fadeOut()", Math.max(2000, errorText.length * 40));
}

var errors = ["Sorry!", "You're nearly there!", "Close!", "Getting warmer...", "Keep at it!", 
"Try lower case...", "Oops!", 
"You're not trying at all, are you.", "Not bad.", "Huh.. never thought of that.", "Really?", 
"You have beautiful eyes.", "You own my favorite pair of legs.", "Bedroom. Now.", 
"Wow, that's clever... not the right answer though.", 
"Maybe you should try a magic dance.", "Getting cooler...", "You're on the right track...", 
"2 attempts remaining.", "3 attempts remaining.", "Not even close.", "Maybe you'd have more luck not wearing pants?",
"You is doing nothing if you is not trying.", "Ever tried. Ever failed. No matter. Try Again. Fail again. Fail better.",
"When there's no wind, row.", "Words are not enough, send candy!", "Yes is one of my favorite answers!", 
"If you think you can't...you're right.", 
"If one advances confidently in the direction of his dreams, and endeavors to live the life which he has imagined, \
he will meet with a success unexpected in the common hours.",
"The way to accelerate your successes is to double your failure rate.",
"It's only a matter of time.", "Don't consider this a rejection... think of it as a chance to improve.",
"Do or do not, there is no try.", "It's always too early to quit.", "Just keep swimming!", 
"Some days are just more tumbly than others.", "Success is buried in the garden of failure.",
"Success isn't final, failure isn't fatal. What counts is the courage to continue.", "Never say die!",
"Perseverance is failing nineteen times and succeeding the twentieth.", 
"Knowing is not enough, we must do. Willing is not enough, we must apply.",
"Don’t fear failure. Not failure, but low aim, is the crime. In great attempts it is glorious even to fail.",
"fall down 7 get up 8.", "Hurry up!", "One minute remaining...", "Encouraging Message Goes Here.", "Oooh, sneaky!",
"I like it!", "Are you sure?", "You are a valuable part of the team.", 
"It is okay to make a mistake, we all do. What do you think you learned from it?", "How can we turn this into a positive?",
"I'm proud of you for trying.", "I know you are disappointed that you didn’t win, but you’ll do better next time.",
"You are really showing improvement.", "I have faith in your ability.", "Don't strain yourself.",
"Struggling? Maybe a quick run would clear your head.", "Neep!", "You must cut down the largest tree in the forest wiiiith... a herring!",
"Vegetables are good for you.", "Han shot first!", "Did you read the prompt?", "Maybe you could try Google?",
"Maybe you could try AskReddit?", "But the real question is, 'why haven't we had sex yet?'",
"Not that you care. Right?", "You smell!... goooood.", "Oooh, I love the sound of typing... more!", 
"Bingely Bongely Beep!", "Drat.", "Doh!", "This mortal form grows weak!", "Perhaps you should try again tomorrow.",
"Please don't give up! You're so close!", "That does not compute!", "Nuh.", 
"Unfortunately, one does not think that that is the correct answer.", "Maybe you should ask someone for help.",
"Did you think of that all by yourself?", "Oh, bravo, bravo, nearly there now..", "Mmmmm, five kinds of wrongness...",
"If you want to build a ship, don’t drum up people together to collect wood and don’t assign them tasks and work, but rather teach them to long for the endless immensity of the sea.",
"Didn't you try that one already?", "Help help help I'm stuck in a computer factory and I can't get out",
"What is this place?", "The best bit of advice I ever received was: 'no-one is going to help you.'",
"Drop and give me 20!", "Your punishment: 10 star jumps, right now.", "I believe in you.", "Is this making you hungry?",
"Wow, you've got stamina.", "Better luck next time.", "Don't take it personally.", "Most people are."
]; 
function randomError() {
	return errors[Math.floor(Math.random()*errors.length)];
}
	

// returns (encodedLink, checksum)
// call from console when creating the puzzles
var maxDecodedLinkLength = 8;
function encode(decodedLink, riddleAnswer) {
	//while (riddleAnswer.length < maxDecodedLinkLength) riddleAnswer += " ";
	var encodedLink = xor_str(decodedLink, riddleAnswer);
	var checkSum = hash_str(riddleAnswer);
	return new Array(btoa(encodedLink), btoa(checkSum));	
}
console.log("function encode(decodedLink, riddleAnswer) :: encodedLink, checkSum");

// uses the provided riddle answer to decode the encodedLink. 
// If the checksum does not match, returns "".
function decode(encodedLink, checkSum, riddleAnswer) {
	//while (riddleAnswer.length < maxDecodedLinkLength) riddleAnswer += " ";
	if (hash_str(riddleAnswer) != atob(checkSum))
		return "";
	return xor_str(atob(encodedLink), riddleAnswer);
}

// loops through the shorter string
function xor_str(strLong, strShort) {
	var result = "";
	var len = strLong.length;
	for (i=0; i < len; i++)
		result += String.fromCharCode(strLong.charCodeAt(i%strLong.length) ^ strShort.charCodeAt(i%strShort.length));
	return result;
}

// This hash function is not at all cryptographically secure. Use a better one if this might matter.
function hash_str(strA) {
	var x = strA.charCodeAt(0) << 7;	
	for(i = 0; i < strA.length; ++i) {		
	    x = (1000003*x) ^ strA.charCodeAt(i);
	}
    x ^= strA.length;	
	return x.toString();
}

function test() {
	var encchk = encode("mOO", "a cow!");
	if (decode(encchk[0], encchk[1], "a cow!") != "mOO")
		return false;
	encchk = encode("for science", "feyn");
	if (decode(encchk[0], encchk[1], "feyn") != "for science")
		return false;
	encchk = encode("12345678", "123456abc");
	if (decode(encchk[0], encchk[1], "123456abc") != "12345678")
		return false;
		
	var counts = {};	
	for (i=0; i < 10000; ++i) 
	{
		var n = Math.floor(Math.random()*97);
		counts[n] ? counts[n] += 1 : counts[n] = 1;
	}
	
	return true;
}
