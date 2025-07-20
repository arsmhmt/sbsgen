$(document).ready(function () {
  // Load sports
  $.get("/api/sports", function (data) {
    const $sports = $("#sportsSelect");
    data.forEach(sport => $sports.append(new Option(sport.name, sport.name)));
  });

  // Load leagues
  $.get("/api/leagues", function (data) {
    const $leagues = $("#leaguesSelect");
    data.forEach(item => {
      const name = item.league.name;
      const country = item.country.name;
      $leagues.append(new Option(`${country} – ${name}`, item.league.id));
    });
  });

  // Load markets
  $.get("/api/markets", function (data) {
    const $markets = $("#marketsSelect");
    data.forEach(market => $markets.append(new Option(market, market)));
  });
});
$(document).ready(function () {
  // Fetch sports
  $.get("/api/sports", function (data) {
    const $select = $("#sportsSelect");
    $select.empty();
    data.forEach(s => $select.append(new Option(s.name, s.name)));
  });

  // Fetch leagues
  $.get("/api/leagues", function (data) {
    const $select = $("#leaguesSelect");
    $select.empty();
    data.forEach(l => $select.append(new Option(`${l.country.name} - ${l.name}`, l.league.id)));
  });

  // TODO: Add markets

  // Generate Betslip button
  $("#generateBetslipBtn").on("click", function () {
    // Gather form data
    const league_ids = $("#leaguesSelect").val() || [];
    const min_odd = $("#minOddInput").val();
    const max_odd = $("#maxOddInput").val();
    const num_matches = $("#matchCountInput").val();

    // Disable button and show loading
    const $btn = $(this);
    $btn.prop("disabled", true).text("Generating...");

    $.ajax({
      url: "/api/betslip",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ league_ids, min_odd, max_odd, num_matches }),
      success: function (resp) {
        // Show betslip preview
        let html = "";
        if (resp.slip && resp.slip.length) {
          resp.slip.forEach(function (m, i) {
            html += `<div class='betslip-match'><span class='fw-bold'>${i+1}.</span> ${m.home_team} vs ${m.away_team} <span class='betslip-odds'>${m.best_odd.value}</span></div>`;
          });
        } else {
          html = "<div class='text-muted text-center'>No matches found.</div>";
        }
        $("#betslipTicketBody").html(html);
        $("#totalOdds").text(resp.total_odds || "--");
        $("#winProb").text(resp.win_probability || "--");
      },
      error: function (xhr) {
        $("#betslipTicketBody").html(`<div class='text-danger text-center'>${xhr.responseJSON?.detail || "Error generating betslip."}</div>`);
        $("#totalOdds").text("--");
        $("#winProb").text("--");
      },
      complete: function () {
        $btn.prop("disabled", false).text("Generate Betslip");
      }
    });
  });
});
