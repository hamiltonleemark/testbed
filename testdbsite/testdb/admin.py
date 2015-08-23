# (c) 2015 Mark Hamilton, <mark_lee_hamilton@att.net>
#
# This file is part of testbed
#
# Testbed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Testbed is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Testdb.  If not, see <http://www.gnu.org/licenses/>.
"""
 Admin interface to test models.
"""
from django.contrib import admin

# Register your models here.
from . import models


class ContextAdmin(admin.ModelAdmin):
    """ View test context content. """
    model = models.Context


class KeyAdmin(admin.ModelAdmin):
    """ View key. """
    model = models.Key


class TestKeyAdmin(admin.ModelAdmin):
    """ View Test Key. """
    model = models.TestKey


class TestAdmin(admin.ModelAdmin):
    """ Show test. """
    model = models.Test


class TestsuiteNameAdmin(admin.ModelAdmin):
    """ Show testsuite name. """
    model = models.TestsuiteName


class TestInlineAdmin(admin.TabularInline):
    """ Show tests inline. """
    model = models.Test
    extra = 0


class TestsuiteFileInlineAdmin(admin.TabularInline):
    """ Show files associated to testsuite inline. """
    model = models.TestsuiteFile
    extra = 0


class TestsuiteKeySetInlineAdmin(admin.TabularInline):
    """ Show set of keys that associate a testsuite. """
    model = models.TestsuiteKeySet
    extra = 0


class TestsuiteAdmin(admin.ModelAdmin):
    """ Show testsuite. """
    model = models.Testsuite
    list_display = ("context", "name", "timestamp")
    date_hierarchy = "timestamp"
    search_fields = ("context", "name", "timestamp")

    inlines = [TestsuiteKeySetInlineAdmin, TestsuiteFileInlineAdmin,
               TestInlineAdmin]


class TestplanAdmin(admin.ModelAdmin):
    """ Administrate testplan content. """
    model = models.Testplan
    extra = 0

    list_display = ("order", "context", "name", "branch")
    def context(self, testplan):
        return testplan.testsuite.context

    def name(self, testplan):
        return testplan.testsuite.name

    def branch(self, testplan):
        return testplan.key_get("branch")


admin.site.register(models.Context, ContextAdmin)
admin.site.register(models.Key, KeyAdmin)
admin.site.register(models.Test, TestAdmin)
admin.site.register(models.TestKey, TestKeyAdmin)
admin.site.register(models.TestsuiteName, TestsuiteNameAdmin)
admin.site.register(models.Testsuite, TestsuiteAdmin)
admin.site.register(models.Testplan, TestplanAdmin)
