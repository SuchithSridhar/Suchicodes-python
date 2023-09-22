function extractDomains(text) {
    // Regular expression to match domain names ending with .info, .com, .net, or .org
    const domainPattern = /\b([a-zA-Z0-9.-]+(?:\.info|\.com|\.net|\.org))\b/g;

    const httpPattern =  /https?:\/\/(?:www\.)?([-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b)(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)/g;
    
    // Domains to exclude
    const excludeList = ["suchicodes.com", "google.com"];
    
    let domains = [];
    let match;

    // Extract domains
    while ((match = domainPattern.exec(text)) !== null) {
        domains.push(match[1]);
    }

    while ((match = httpPattern.exec(text)) !== null) {
        domains.push(match[1]);
    }

    // Remove duplicates and exclude specific domains
    domains = [...new Set(domains)].filter(domain => !excludeList.includes(domain));

    return domains;
}

function delete_message(message_id) {
    $.ajax({
      url: `/admin/message/delete/${message_id}`,
      success: (result) => {
        alert(result);
        $(`.message-row[data-id='${message_id}']`).remove();
      }
    })

}

function block_domains(message_id) {
    let subject = $(`.message-row[data-id='${message_id}'] [data-type='message-subject']`).text();
    let message = $(`.message-row[data-id='${message_id}'] [data-type='message-body']`).text();
    let domains = extractDomains(`${subject} ${message}`);

    if (confirm(`Block domains: [${domains}]?`)){
      domains.forEach(domain => {
        let url = `/admin/blacklist?type=message&message=${domain}`;
        $.ajax({
          url: url,
          success: (result) => {
            alert(result);
          },
        });
      })
    }
}

function initialize() {
  $('.block-ip-button').click(e => {
    let target = $(e.currentTarget);
    let ip = target.attr('data-ip');

    if (confirm(`Block ip: '${ip}'?`)){
      let url = `/admin/blacklist?type=ip&ip=${ip}`;
      $.ajax({
        url: url,
        success: (result) => {
          alert(result);
        },
      });
    }
  });

  $('.block-domain-button').click(e => {
    let target = $(e.currentTarget);
    let id = target.attr('data-id');
    block_domains(id);
  })

  $('.delete-message-button').click(e => {
    let target = $(e.currentTarget);
    let id = target.attr('data-id');
    if (confirm("Are you sure you want to delete the message?")) {
      delete_message(id);
    }
  })

  $('.block-message').click(e => {
    let target = $(e.currentTarget);
    let message = $("#block-message").val().trim();
    let url = `/admin/blacklist?type=message&message=${message}`;

    if (message === ""){
      return;
    }

    if (confirm("Are you sure you want to black list the this message?")){
      $.ajax({
        url: url,
        success: (result) => {
          alert(result);
        },
      });
    }
  });
}

$(document).ready(() => {
  initialize();
});
