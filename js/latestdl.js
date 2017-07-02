/*jslint browser: true*/
/*global $, jQuery, alert*/

"use strict";

function GetLatestReleaseInfo() {
    $.getJSON("{{site.github.api_url}}/repos/{{site.github.owner_name}}/{{site.github.repository_name}}/releases/latest").done(function (release) {
        var asset = release.assets[0];
        var downloadCount = 0;
        for (var i = 0; i < release.assets.length; i++) {
            downloadCount += release.assets[i].download_count;
        }
        var oneHour = 60 * 60 * 1000;
        var oneDay = 24 * oneHour;
        var dateDiff = new Date() - new Date(asset.updated_at);
        var timeAgo;
        if (dateDiff < oneDay) {
            timeAgo = (dateDiff / oneHour).toFixed(1) + " hours ago";
        } else {
            timeAgo = (dateDiff / oneDay).toFixed(1) + " days ago";
        }
        var releaseInfo = "Version: " + release.tag_name.substring(1) + "\nReleased: " + timeAgo + "\nDownload count: " + downloadCount.toLocaleString();
        $(".latest_release_dl").attr("href", asset.browser_download_url);
        $(".latest_release_dl").attr("title", "<a href='downloads/'><div>" + releaseInfo + "</div></a>");

        InitTooltip($(".latest_release_dl"));
    });
}

function InitTooltip(obj, fadeDelay = 300) {
    obj.tooltip({
        trigger: "manual",
        html: true,
        animation: false
    }).on("mouseenter", function () {
        obj.tooltip("show");
    }).on("mouseleave", function () {
        setTimeout(function () {
            if (!obj.is(":hover") && !$(".tooltip").is(":hover")) {
                obj.tooltip("hide");
            }
        }, fadeDelay);
    });

    obj.parent().on("mouseleave", ".tooltip", function () {
        setTimeout(function () {
            if (!obj.is(":hover") && !$(".tooltip").is(":hover")) {
                obj.tooltip("hide");
            }
        }, fadeDelay);
    });

    if (obj.is(":hover")) {
        obj.tooltip("show");
    }
}

$(document).ready(function () {
    GetLatestReleaseInfo();
});
