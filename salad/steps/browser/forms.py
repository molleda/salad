from time import sleep
from lettuce import step, world
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.errorhandler import StaleElementReferenceException
from salad.steps.browser.finders import (PICK_EXPRESSION, ELEMENT_FINDERS, ELEMENT_THING_STRING,
        _get_visible_element, _convert_pattern_to_css)
from salad.tests.util import assert_equals_with_negate

# What's happening here? We're generating steps for every possible permuation of the element finder

for finder_string, finder_function in ELEMENT_FINDERS.iteritems():

    def _type_generator(finder_string, finder_function):
        @step(r'(slowly )?type "([^"]*)" into the%s %s %s' % (
                PICK_EXPRESSION, ELEMENT_THING_STRING, finder_string))
        def _this_step(step, slowly, text, pick, find_pattern):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            if slowly and slowly != "":
                _type_slowly(ele, text)
            else:
                ele.value = text

        return _this_step

    globals()["form_type_%s" % (finder_function,)] = _type_generator(finder_string, finder_function)


    def _select_generator(finder_string, finder_function):
	@step(r'select the option (named|with the value)? "([^"]*)" (?:from|in) the( first)?( last)? %s %s' % (
                ELEMENT_THING_STRING, finder_string))
	def _this_step(step, named_or_with_value, field_value, first, last, find_pattern):
		css = _convert_pattern_to_css(finder_function, first, last, find_pattern, tag="select")

		if named_or_with_value == "with the value":
			css += " option[value='%s']" % (field_value,)
			ele = world.browser.find_by_css(css).first
		else:
			ele = world.browser.find_option_by_text(field_value)

		ele.click()

	return _this_step

    globals()["form_select_%s" % (finder_function,)] = _select_generator(finder_string, finder_function)

    def _fill_generator(finder_string, finder_function):
        @step(r'fill in the( first| last)? %s %s with "([^"]*)"' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, pick, find_pattern, text):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            try:
                ele.value = text
            except:
                ele._control.value = text

        return _this_step

    globals()["form_fill_%s" % (finder_function,)] = _fill_generator(finder_string, finder_function)

    def _type_generator(finder_string, finder_function):
        @step(r'(slowly )?type "([^"]*)" into the( first)?( last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, slowly, text, first, last, find_pattern):
            css = _convert_pattern_to_css(finder_function, first, last, find_pattern)

# try to use _get_visible_element
# i get a splinter element that has a selenium element as attribute
# the driver here is selenium or the selenium browser
            driver_ele = world.browser.driver.find_element_by_css_selector(css)
            if slowly and slowly != "":
                TypeIterator(driver_ele, text)
            else:
                driver_ele.send_keys(text)

        return _this_step

    globals()["form_type_%s" % (finder_function,)] = _type_generator(finder_string, finder_function)

    def _attach_generator(finder_string, finder_function):
        @step(r'attach "([^"]*)" onto the( first| last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, file_name, pick, find_pattern):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            try:
                ele.value = file_name
            except:  # Zope
                ele._control.value = file_name

        return _this_step

    globals()["form_attach_%s" % (finder_function,)] = _attach_generator(finder_string, finder_function)

    def _select_generator(finder_string, finder_function):
        @step(r'select the option (named|with the value)? "([^"]*)" (?:from|in) the( first)?( last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, named_or_with_value, field_value, first, last, find_pattern):
            css = _convert_pattern_to_css(finder_function, first, last, find_pattern, tag="select")

            if named_or_with_value == "with the value":
                css += " option[value='%s']" % (field_value,)
                ele = world.browser.find_by_css(css).first
            else:
                ele = world.browser.find_option_by_text(field_value)

            ele.click()

        return _this_step

    globals()["form_select_%s" % (finder_function,)] = _select_generator(finder_string, finder_function)

    def _focus_generator(finder_string, finder_function):
        @step(r'focus on the( first| last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, pick, find_pattern):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            ele.focus()

        return _this_step

    globals()["form_focus_%s" % (finder_function,)] = _focus_generator(finder_string, finder_function)

    def _blur_generator(finder_string, finder_function):
        @step(r'(?:blur|move) from the( first| last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, pick, find_pattern):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            ele.blur()

        return _this_step

    globals()["form_blur_%s" % (finder_function,)] = _blur_generator(finder_string, finder_function)

    def _value_generator(finder_string, finder_function):
        @step(r'(?:should see that the)? value of the( first| last)? %s %s is( not)? "([^"]*)"' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, pick, find_pattern, negate, value):
            ele = _get_visible_element(finder_function, pick, find_pattern)
            assert_equals_with_negate(ele.value, value, negate)

        return _this_step

    globals()["form_value_%s" % (finder_function,)] = _value_generator(finder_string, finder_function)

    def _key_generator(finder_string, finder_function):
        @step(r'hit the ([^"]*) key in the ( first| last)? %s %s' % (ELEMENT_THING_STRING, finder_string))
        def _this_step(step, pick, find_pattern):
            key = transform_key_string(key_string)
            ele = _get_visible_element(finder_function, pick, find_pattern)
            ele.type(key)

        return _this_step

    globals()["form_key_%s" % (finder_function,)] = _key_generator(finder_string, finder_function)


@step(r'hit the ([^"]*) key')
def hit_key(step, key_string):
    key = transform_key_string(key_string)
    try:
        world.browser.driver.switch_to_active_element().send_keys(key)
    except StaleElementReferenceException:
        world.browser.find_by_css("body").type(key)

def transform_key_string(key_string):
    key_string = key_string.upper().replace(' ', '_')
    if key_string == 'BACKSPACE':
        key_string = 'BACK_SPACE'
    elif key_string == 'SPACEBAR':
        key_string = 'SPACE'
    key = Keys.__getattribute__(Keys, key_string)
    return key

def _type_slowly(driver_ele, text):
    for c in text:
        driver_ele.value += c
        sleep(0.5)

