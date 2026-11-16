# Runs inside a fresh Discourse container.
SiteSetting.wizard_enabled = false
SiteSetting.force_https = false
SiteSetting.must_approve_users = false
SiteSetting.login_required = false
reader = User.create!(username: "ci_reader", name: "CI Reader",
                      email: "reader@example.invalid", password: ENV.fetch("FIXTURE_PASSWORD"),
                      active: true, approved: true, trust_level: 1)
reader.activate
["CI read receipt target", "CI unread control topic"].each do |title|
  PostCreator.create!(Discourse.system_user, title: title, raw: "A single fixture post for the browser read receipt test.",
                      category: SiteSetting.uncategorized_category_id, skip_validations: true)
end
