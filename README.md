# .github

Default [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) and profile page for the [Avic-AI](https://github.com/Avic-AI) organization.

Files in this repository are inherited by every repository in the org that doesn't provide its own copy:

- **CODE_OF_CONDUCT.md**: Contributor Covenant v2.1
- **CONTRIBUTING.md**: contribution guidelines and PR checklist
- **SECURITY.md**: vulnerability reporting policy
- **FUNDING.yml**: sponsor links
- **Issue and PR templates**: bug reports, feature requests, PR checklist

`profile/README.md` is the org landing page. The block between the
`public-repos` markers is rewritten daily by
`.github/workflows/profile-repos.yml`. It lists **public** repositories
only, so a private repo never appears and a repo shows up on its own once it
is made public.

Renovate settings come from the shared preset in
[Avicennasis/.github](https://github.com/Avicennasis/.github). It is not
copied here.
