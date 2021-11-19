// This is an array of objects that stores the personality trait that is prompted to the user and the weight for each prompt. 
// If a personality trait is considered more introverted, it will have a negative weight.
// If a personlity trait is considered more extroverted, it will have a positive weight.

var prompts = [
	{
		prompt: 'I find it difficult to introduce myself to people',
		weight: -1,
		class: 'group0'
	},
	{
		prompt: 'I get so lost in my thoughts I ignore or forget my surroundings',
		weight: -1,
		class: 'group1'
	},
	{
		prompt: 'I do not usually initiate conversations',
		weight: -1,
		class: 'group2'
	},
	{
		prompt: 'I prefer not to engage with people who seem angry or upset',
		weight: -1,
		class: 'group3'
	},
	{
		prompt: 'I choose my friends carefully',
		weight: -1,
		class: 'group4'
	},
	{
		prompt: 'I find it difficult to tell stories about myself',
		weight: -1,
		class: 'group5'
	},
	{
		prompt: 'I am usually highly motivated and energetic',
		weight: 1,
		class: 'group6'
	},
	{
		prompt: 'I find it easy to walk up to a group of people and join a conversation',
		weight: 1,
		class: 'group7'
	},
	{
		prompt: 'Being adaptable is more important than being organized',
		weight: 1,
		class: 'group8'
	},
	{
		prompt: 'I care more about making sure no one gets upset, than being right',
		weight: 1,
		class: 'group9'
	},
	{
		prompt: 'I often feel that I have to justify myself to people',
		weight: -1,
		class: 'group10'
	},
	{
		prompt: 'I would rather improvise than spend time coming up with a detailed plan',
		weight: 1,
		class: 'group11'
	}
]

// This array stores all of the possible values and the weight associated with the value. 
// The stronger agreeance/disagreeance, the higher the weight on the user's answer to the prompt.
var prompt_values = [
	{
		value: 'Strongly Disagree',
		class: 'btn-default btn-strongly-disagree',
		weight: -5
	},
	{
		value: 'Disagree',
		class: 'btn-default btn-disagree',
		weight: -3
	},
	{
		value: 'Neutral',
		class: 'btn-default',
		weight: 0
	},
	{
		value: 'Agree',
		class: 'btn-default btn-agree',
		weight: 3,
	},
	{
		value: 'Strongly Agree',
		class: 'btn-default btn-strongly-agree',
		weight: 5
	}	
]

var showTriple = prompts.slice(0, 3);
var outputNumber = '';
var nextPrev = 0;
var btn_3 = 3;
var total = 0;
var elementClicked;

var result = document.querySelector('.result');
var cmp = document.getElementById('page');
$('.next').show();
$('.submitBtn').hide();
$('.retake').hide();

// For each prompt, create a list item to be inserted in the list group
function createPromptItems(myList) {

	var replace = document.getElementById('quiz');
	while (replace.firstChild) {
		replace.removeChild(replace.lastChild);
	}

	for (var i = 0; i < myList.length; i++) {
		var prompt_li = document.createElement('li');
		var prompt_p = document.createElement('p');
		var prompt_text = document.createTextNode(myList[i].prompt);

		prompt_li.setAttribute('class', 'list-group-item prompt');
		prompt_p.appendChild(prompt_text);
		prompt_li.appendChild(prompt_p);

		document.getElementById('quiz').appendChild(prompt_li);
	}
}

function createValueButtons(myList) {

	for (var li_index = 0; li_index < myList.length; li_index++) {
		var group = document.createElement('div');
		group.className = 'btn-group btn-group-justified';

		for (var i = 0; i < prompt_values.length; i++) {
			var btn_group = document.createElement('div');
			btn_group.className = 'btn-group';

			var button = document.createElement('button');
			var button_text = document.createTextNode(prompt_values[i].value);
			button.className = 'group' + li_index + ' value-btn btn ' + prompt_values[i].class;
		
			button.appendChild(button_text);
			btn_group.appendChild(button);
			group.appendChild(btn_group);
			document.getElementsByClassName('prompt')[li_index].appendChild(group);
			
		}
	}
}


/* function prev() {
	nextPrev--;
	cmp.innerHTML = parseInt(cmp.innerHTML) - 1;
	btn_3 -= 3;
	showTriple = prompts.slice(btn_3-3, btn_3);
	
	createPromptItems(showTriple);
	createValueButtons(showTriple);	
	if (nextPrev == 0) {
	   $('.prev').hide();
	}
} */

function retake() {
	window.location.reload();
}

function next() {
	if (nextPrev == 3) {
		$('.next').hide();
		$('.submitBtn').show();
		$('.retake').show();
	}  else {

		nextPrev++;
		console.log(nextPrev);
		cmp.innerHTML = parseInt(cmp.innerHTML) + 1;
		showTriple = prompts.slice(btn_3, btn_3 + 3);
		btn_3 += 3;
		createPromptItems(showTriple);
		createValueButtons(showTriple);
	} 
}



// Get the weight associated to group number
function findPromptWeight(prompts, group) {
	var weight = 0;
	for (var i = 0; i < prompts.length; i++) {
		if (prompts[i].class === group) {
			weight = prompts[i].weight;
		}
	}
	return weight;
}


// Get the weight associated to the value
function findValueWeight(values, value) {
	var weight = 0;

	for (var i = 0; i < values.length; i++) {
		if (values[i].value === value) {
			weight = values[i].weight;
		}
	}
	return weight;
}

function addScore(myList) {
	$(document).on('mousedown', '.value-btn', function () {
		var classList = $(this).attr('class');
		var classArr = classList.split(" ");
		var this_group = classArr[0];

		//console.log('ClassList ' + classList + '\tclassArr ' + classArr + '\tThis group ' + this_group);
		// If button is already selected, de-select it when clicked and subtract any previously added values to the total
		// Otherwise, de-select any selected buttons in group and select the one just clicked
		// And subtract deselected weighted value and add the newly selected weighted value to the total

		if ($(this).hasClass('active')) {
			$(this).removeClass('active');
			total -= (findPromptWeight(myList, this_group) * findValueWeight(prompt_values, $(this).text()));
			// console.log("Total remove active" + " " + total);
		} else {
			$('.' + this_group).prop('checked', false);
			total -= (findPromptWeight(myList, this_group) * findValueWeight(prompt_values, $('.' + this_group + '.active').text()));
			// console.log("Total change group" + " " + total);
			// console.log($('.'+this_group+'.active').text());
			$('.' + this_group).removeClass('active');
			$(this).prop('checked', true);
			$(this).addClass('active');
			total += (findPromptWeight(myList, this_group) * findValueWeight(prompt_values, $(this).text()));
			// console.log("Total add active" + " " + total);
		}
		console.log(total);
	})
}

function submitTotalScore() {
	if (total > -20 && total < -10) {
		outputNumber = 1;
	} else if (total >= -10 && total < 0) {
		outputNumber = 2;
	} else if (total >= 0 && total < 10) {
		outputNumber = 3;
	} else if (total >= 10 && total < 20) {
		outputNumber = 4;
	} else if (total >= 20) {
		outputNumber = 5;
	}
	$.post("/postmethod", {
		javascript_data: outputNumber
	});

	window.location.href ="/takeVideo";

}

createPromptItems(showTriple);
createValueButtons(showTriple);
addScore(showTriple);
