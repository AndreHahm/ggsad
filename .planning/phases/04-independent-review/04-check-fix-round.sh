#!/usr/bin/env bash
# Read-only check of the fix round that follows the independent review of the proposed normative method
# specification: the pins of the text of round 1, whether the live specification still equals them, the replay
# of the three round-1 checks at the commit that holds the round-1 text, the record of the five owner
# decisions D-1 to D-5 with the printers of its questions and of its skeleton, the edits of the fix round
# with the register that lists them, and the owner approval of the exact new text with the printers of the
# packet, of its questions, of the exact change and of the skeleton of the record. Profile 5 adds the disposition
# addendum of round 4 (its printer and its checks DA1 to DA5), the changes of fix round 5 and the approval of the
# exact new text (plan 04-19). Profile 6 (plan 04-22) is profile 5 one level up: the disposition addendum of round 5,
# the changes of fix round 6 and the stages edits and dispositions (plan 04-22); plan 04-23 adds the approval stages and
# the approval printers to profile 6. Profile 7 (plans 04-26 and 04-27) is profile 6 one level up and reads no
# addendum: every disposition of round 6 is in the disposition record; plan 04-26 adds the stage edits to it.
#
# Usage: 04-check-fix-round.sh [options]
#   --stage STAGE     state (default): ST1 and the fact line ST2; decisions: FD1 to FD8 on the decisions
#                     record; edits: FE1 to FE6 on the specification and the fix register; approval-pending:
#                     AP1 to AP5 on the diff identity note and the approval packet; approval-recorded: AR1 to
#                     AR5 on the approval record and the packet. The list of stages is open
#   --packet PATH     the approval packet of the fix round (default: the packet path of the repository)
#   --record PATH     the approval record of the fix round (default: the record path of the repository)
#   --identity PATH   the diff identity note (default: the note path of the repository); a test hook
#   --approval-record PATH
#                     the owner approval record of round 1 (default: the record path of the repository;
#                     relative paths are taken from the repository root)
#   --disposition-record PATH
#                     the review disposition record of round 1 (default: the record path of the repository)
#   --decisions PATH  the record of the owner decisions, read in stage decisions (default: the record path of
#                     the repository)
#   --spec PATH       the specification file to hash or to judge (default: the specification path of the
#                     repository); a test hook that replaces the working file for the hash reads and for the
#                     stage edits only, the index and HEAD reads always use the real path
#   --register PATH   the fix register, read in stage edits (default: the register path of the repository)
#   --complete        modifier of --stage edits: all nine groups must be drafted and the Findings cells of the
#                     register must cover exactly the eleven findings with the disposition fix
#   --base REF        base ref of the diff (default origin/main); must name a commit; in the replay the
#                     remote-tracking ref origin/main of the throwaway clone is set to this commit
#   --replay-round-1  run FR1 to FR4 instead of a stage (no other check runs): FR1 the newest commit reachable
#                     from HEAD at which the specification holds the round-1 blob is found (a commit that does
#                     not touch the specification counts) and holds the approval record and the disposition
#                     record; the commit is never printed. A throwaway clone of the repository is made outside
#                     the repository (a local clone, not a worktree), the commit is checked out detached in it
#                     and origin/main of the clone is aligned; there, with the scripts as they are at that
#                     commit, FR2 the drafting check with --final, FR3 the owner approval check in stage
#                     recorded, FR4 the review check in stage dispositioned each end RESULT: PASS. The clone is
#                     removed on exit; the repository and its refs are not changed
#   --with-current-scripts
#                     modifier of --replay-round-1: the working-tree versions of the three scripts are copied
#                     over the three paths in the clone and the three runs are repeated as FR5 (a later
#                     extension of a script still validates the round-1 evidence); the same modifier of
#                     --replay-round-2, --replay-round-3 and --replay-round-5 repeats the six runs as R2-8, R3-8
#                     and R5-8
#   --print-decision-questions
#                     print the five decisions as the owner is asked them: a line with the id and the header,
#                     a line Findings:, the question on one line, one line per option "- label: description"
#                     (the label is the text before the first colon followed by a space), and a blank line
#                     between decisions; exit 0
#   --print-register-skeleton
#                     print the skeleton of the fix register (the only way the register is created): the nine
#                     groups with the status pending and the 14 findings that the owner did not disposition;
#                     exit 0 (exit 2 if the review note cannot be read)
#   --print-decisions-skeleton
#                     print the skeleton of the decisions record (the only way the record is created); every
#                     field that the owner completes holds the fill marker (@@FILL@@); exit 0 (exit 2 if the
#                     records of round 1 cannot be read)
#   --print-delta     print the hunks of the change from the text approved in round 1 to the working
#                     specification, starting at the first line that begins with @@; exit 2 if the two texts
#                     are equal
#   --print-approval-questions
#                     print the four questions of the owner approval in plain words: a line "Q0n header", the
#                     question on one line and, for the first, one line "label: description" per option
#   --print-approval-packet
#                     print the approval packet in its pending form from the live specification, the register
#                     and the records of round 1 (the only way the packet is created); exit 2 if the register
#                     is not complete or the texts are equal
#   --print-approval-record-skeleton
#                     print the approval record in its unfilled form for the packet (the only way the record
#                     is created); every field the owner completes holds the fill marker; exit 2 if the packet
#                     status line is not the pending form
#   --addendum PATH   the disposition addendum, read in profiles 5 and 6 (the addendum of round 4 in profile 5, the
#                     addendum of round 5 in profile 6; default: the addendum path of the profile; relative paths
#                     are taken from the repository root)
#   --print-addendum-skeleton
#                     print the disposition addendum in its unfilled form (the only way the addendum is created):
#                     the pin rows copied from the disposition record of the review that the addendum answers
#                     (round 4 in profile 5, round 5 in profile 6), one block for each finding of --findings as
#                     the review check script prints it (the question is never typed here), the reply details and
#                     the fixed text; every field the owner or the executor completes holds the fill marker;
#                     exit 0 (exit 2 for any round but 5 and 6 and when the review note or a record cannot be read)
#   --findings LIST   modifier of --print-addendum-skeleton: a comma-separated list of finding ids of the review
#                     note (default: RF-B-004,RF-X-002,RF-X-003,RF-X-004 in profile 5, RG-C-001,RG-X-001,RG-X-004
#                     in profile 6); the blocks are printed in the order of the findings table; an id that the
#                     disposition record dispositions, that the note does not hold or that occurs twice exits 2
#   --round N         the round profile: 2 (default) holds every value that this script has always held (the
#                     fix round that follows the first independent review); 3 is the profile of the fix round
#                     that follows the second independent review (plans 04-10 and 04-11); 4 is the profile of
#                     the fix round that follows the third independent review (plans 04-14 and 04-15); 5 is the
#                     profile of the fix round that follows the fourth independent review (plans 04-18 and
#                     04-19); 6 is the profile of the fix round that follows the fifth independent review (plans
#                     04-22 and 04-23); 7 is the profile of the fix round that follows the sixth independent
#                     review (plans 04-26 and 04-27); any other value exits 2. Profile 3 reads the approval record, the disposition record and the
#                     review note of the second round, finds the findings with the prefix RR, has three
#                     changes FG-10 to FG-12 and nine findings without a disposition, and allows the stages
#                     edits, approval-pending and approval-recorded (the stage defaults to edits; the stages
#                     state and decisions and the printer of the decisions record exit 2). Profile 4 reads the
#                     approval record, the disposition record and the review note of the third round, finds
#                     the findings with the prefix RT, has three changes FG-13 to FG-15 and twenty findings
#                     without a disposition, and allows the stages edits, approval-pending and approval-recorded
#                     (the stage defaults to edits; the stages state and decisions and the printer of the
#                     decisions record exit 2). Profile 5 reads the
#                     approval record of round 4, the disposition record of round 4 and its addendum, and the
#                     review note of the fourth round, finds the findings with the prefix RF, has up to seven
#                     changes FG-16 to FG-22 (a change is present only when its primary finding has the
#                     disposition fix in the record or the addendum, so the number of changes is derived),
#                     and allows the stages edits, dispositions, approval-pending and approval-recorded (the stage
#                     defaults to edits; the stages state and decisions and the printer of the decisions record exit
#                     2). The approval stages and the printers --print-delta, --print-approval-questions,
#                     --print-approval-packet and --print-approval-record-skeleton work under --round 5 with the
#                     values of the table below; --addendum names the addendum that the packet pins
#   --replay-round-2  run R2-1 to R2-8 instead of a stage (no other check runs): R2-1 the newest commit
#                     reachable from HEAD at which the specification holds the result blob of the approval
#                     record of the fix round (read from --approval-record, default: the record path of the fix
#                     round) is found and holds that record, the disposition record, the review note, the fix
#                     register, the approval packet and the review brief of round 2; the commit is never
#                     printed. In a throwaway local clone outside the repository, checked out detached at that
#                     commit with origin/main aligned as in the replay of round 1, and with the scripts as they
#                     are at that commit: R2-2 the drafting check with --final, R2-3 this script in stage edits
#                     with --complete, R2-4 this script in stage approval-pending, R2-5 this script in stage
#                     approval-recorded, R2-6 the review check with --round 2 prints the review brief of
#                     round 2 character for character, R2-7 the review check with --round 2 in stage
#                     dispositioned each end RESULT: PASS (R2-6: equal). With --with-current-scripts the
#                     working-tree versions of the three scripts are copied over their paths in the clone and
#                     the six runs are repeated as R2-8. The clone is removed on exit; the repository and its
#                     refs are not changed. It cannot be combined with --replay-round-1 (exit 2)
#   --replay-round-3  run R3-1 to R3-8 instead of a stage (no other check runs): R3-1 the newest commit
#                     reachable from HEAD at which the specification holds the result blob of the approval
#                     record of the fix round of round 3 (read from --approval-record, default: the record path
#                     of fix round 3) is found and holds that record, the disposition record, the review note,
#                     the fix register, the approval packet and the review brief of round 3; the commit is never
#                     printed. In a throwaway local clone outside the repository, checked out detached at that
#                     commit with origin/main aligned as in the replay of round 1, and with the scripts as they
#                     are at that commit: R3-2 the drafting check with --final, R3-3 this script with --round 3
#                     in stage edits with --complete, R3-4 this script with --round 3 in stage approval-pending,
#                     R3-5 this script with --round 3 in stage approval-recorded, R3-6 the review check with
#                     --round 3 prints the review brief of round 3 character for character, R3-7 the review
#                     check with --round 3 in stage dispositioned each end RESULT: PASS (R3-6: equal). With
#                     --with-current-scripts the working-tree versions of the three scripts are copied over their
#                     paths in the clone and the six runs are repeated as R3-8. The clone is removed on exit; the
#                     repository and its refs are not changed. It cannot be combined with --replay-round-1 or
#                     --replay-round-2 (exit 2)
#   --replay-round-5  run R5-1 to R5-8 instead of a stage (no other check runs; the round profile is not
#                     consulted): R5-1 the result blob of the approval record of fix round 5 (read from
#                     --approval-record, default: the record path of fix round 5) is read, the newest commit
#                     reachable from HEAD at which the specification holds that blob is found, and that commit holds
#                     the approval record, the disposition record, the review note, the fix register, the approval
#                     packet and the review brief of round 5 and the disposition addendum of round 4; the commit is
#                     never printed. In a throwaway local clone outside the repository, checked out detached at that
#                     commit with origin/main aligned as in the replay of round 1, and with the scripts as they are
#                     at that commit: R5-2 the drafting check with --final, R5-3 this script with --round 5 in stage
#                     edits with --complete, R5-4 this script with --round 5 in stage approval-pending, R5-5 this
#                     script with --round 5 in stage approval-recorded, R5-6 the review check with --round 5 prints
#                     the review brief of round 5 character for character, R5-7 the review check with --round 5 in
#                     stage dispositioned each end RESULT: PASS (R5-6: equal). With --with-current-scripts the
#                     working-tree versions of the three scripts are copied over their paths in the clone and the six
#                     runs are repeated as R5-8. The clone is removed on exit; the repository and its refs are not
#                     changed. It cannot be combined with --replay-round-1, --replay-round-2, --replay-round-3 or
#                     --replay-round-4 (exit 2). Once the specification no longer holds the text of round 5, the
#                     live checks that pin that text fail by design and this replay is the way to check the evidence
#                     of round 5
#   -h, --help        print this text and exit 0
#
# Profiles 3, 4 and 5 (--round 3, --round 4 and --round 5), used by plans 04-10 and 04-11, by plans 04-14 and
# 04-15 and by plans 04-18 and 04-19. The profile table (round 2 is the default and holds every value this script
# has always held; the column for round 5 lists the values of the register, of the edits and of the approval):
#   value                 round 2                       round 3                       round 4                       round 5                         round 6                         round 7
#   packet, record        the fix round approval        the packet and the record     the packet and the record     the packet and the record       the packet and the record       the packet and the record
#                         packet and record of the      of fix round 3 (2026-10-27-   of fix round 4 (2026-10-27-   of fix round 5 (2026-10-28-     of fix round 6 (2026-10-29-     of fix round 7 (2026-10-30-
#                         repository                    ...-fix-round-3-*)            ...-fix-round-4-*)            ...-fix-round-5-*)              ...-fix-round-6-*)              ...-fix-round-7-*)
#   register              the nine-change register      the register of round 3       the register of round 4       the register of round 5         the register of round 6         the register of round 7
#                                                       (three changes)               (three changes)               (derived number of changes)     (derived number of changes)     (derived number of changes)
#   approval record       the record of round 1         the record of the fix round   the record of fix round 3     the record of fix round 4       the record of fix round 5       the record of fix round 6
#                                                       (round 2)
#   disposition record    the record of round 1         the record of round 2         the record of round 3         the record of round 4 and       the record of round 5 and       the record of round 6 (no
#                                                                                                                   its addendum                    its addendum                    addendum)
#   review note           the note of round 1           the note of round 2           the note of round 3           the note of round 4             the note of round 5             the note of round 6
#   finding ids           RV                            RR                            RT                            RF                              RG                              RH
#   changes               FG-01 to FG-09                FG-10 to FG-12                FG-13 to FG-15                FG-16 to FG-22 (derived)        FG-23 to FG-25 (derived)        FG-26 to FG-28 (derived)
#   undispositioned       14                            9                             20                            33 less the findings of         21 less the findings of         12 rows less 3 dispositioned: 9
#                                                                                                                   the addendum                    the addendum
#   first new example     AE-295                        AE-306                        AE-309                        AE-311                          AE-321                          AE-324
#   text approved before  the text of round 1           the text of round 2           the text of round 3           the text of round 4             the text of round 5             the text of round 6
#   changes in the packet nine, "my choice" or repair   three, "your decision:        three, "your decision:        as many as the register         as profile 5 (plan 04-23        as profile 5 (plan 04-27
#                                                       <label>" with the options     <label>" with the options     holds (derived), shown as       prints it)                      prints it)
#                                                       offered, the decision and     offered, the decision and     in profile 4; the pins
#                                                       its reason                    its reason; for the kind      also name the disposition
#                                                                                     repair "no decision asked:    addendum, and the answers
#                                                                                     the finding names the fix"    on the related findings
#                                                                                                                   are listed
#   kinds of change       repair, my choice             owner decision                owner decision, repair        owner decision, repair          owner decision, repair          owner decision, repair
#   H1 lines              "fix round"                   "fix round 3"                 "fix round 4"                 "fix round 5"                   "fix round 6"                   "fix round 7"
#   stages                all five                      edits, approval-pending,      edits, approval-pending,      edits, dispositions,            as profile 5                    edits (plan 04-26); plan 04-27
#                                                       approval-recorded             approval-recorded             approval-pending,                                               adds approval-pending and
#                                                                                                                   approval-recorded                                               approval-recorded
# The questions Q01 to Q04, their headers and options are the same in all profiles. Under --round 3 and --round 4
# the stages approval-pending and approval-recorded and the printers --print-delta, --print-approval-questions,
# --print-approval-packet and --print-approval-record-skeleton work, with the checks AP1 to AP5 and AR1 to AR5
# as described below. Under --round 3 the lower bound of the date of AR5 is taken from the disposition record of
# round 2 and the previously approved pins are those of the text of round 2; under --round 4 they are taken from the
# disposition record of round 3 and the approval record of round 3; under --round 5 the lower bound is taken from
# the disposition addendum of round 4 and the previously approved pins are those of the approval record of round 4;
# under --round 6 the lower bound is taken from the disposition addendum of round 5 and the previously approved pins
# are those of the approval record of round 5 (profile 6 is used by plans 04-22 and 04-23).
# In the packet of profile 5 the paragraph "What you are asked" says that the reviewer looked at the text a fourth
# time (profile 6: a fifth time, a profile value) and lists the answers of the owner on the related findings as the
# addendum records them (the headings of the addendum carry the id prefix of the profile), the pin table gains
# the rows "Disposition addendum file" and "Disposition addendum blob" after the register rows (the file name is
# the addendum path of the profile), and the changes are shown as in profile 4. In the packet of profile 4 the paragraph "What
# you are asked" says that the reviewer looked at the text a third time and that for the third change the finding
# itself names the fix; a change of the kind repair is shown with the cell "no decision asked: the finding names
# the fix" and the bullet "Your decision: none asked; the finding leaves no design choice", without the bullet
# "Options offered".
#   --print-decision-questions  prints the three decisions OD-1 to OD-3 that the owner is asked: a line with
#                     the id and the header, a line "Finding: ID (SEVERITY)", a line "The reviewer says: " and
#                     the Summary cell of the finding in the findings table of the review note of round 2
#                     verbatim, a line "Question: " and the question, one line "- label: description" per
#                     option (no option is recommended) and a blank line between decisions; exit 0
#   --print-register-skeleton  prints the skeleton of the fix register of round 3 (the only way it is created):
#                     the three changes FG-10 to FG-12 with the status pending and the nine findings that the
#                     owner did not disposition; exit 0
#   Stage edits in profile 3 runs FE3 to FE7 (FE1 and FE2 belong to round 2): FE3 minimality as in round 2 with
#   nine findings without a disposition (the quoted sentence of a finding whose reference names the file BASE
#   is exempt); FE4 as in round 2; FE5 the register with three entries of nine bullets (What changed, Why,
#   Options, Owner decision, Owner reason, Channel, Before, After, Notes), example ids that run on from AE-306
#   and, with --complete, the Findings cells equal to exactly the findings with the disposition fix; FE6 as in
#   round 2; FE7 for each drafted entry the Options bullet equals the printed labels of its decision joined by
#   " | ", the Owner decision is exactly one of them, the Owner reason is non-empty and the Channel is the
#   fixed sentence.
#   Profile 4 (--round 4), used by plans 04-14 and 04-15, differs from profile 3 in values and in one kind of
#   change, nothing more. --print-decision-questions prints the two decisions OD-4 (finding RT-A-001) and OD-5
#   (finding RT-B-001) in the form of profile 3, and --print-register-skeleton prints the skeleton of the fix
#   register of round 4 with the changes FG-13 to FG-15 and the twenty findings that the owner did not
#   disposition. The kind of a change is given by the data function of the script: FG-13 and FG-14 are an owner
#   decision, FG-15 is a repair (its finding leaves no design choice). FE3 expects twenty findings without a
#   disposition; FE5 compares the Kind cell of each entry with the kind that the data function gives for it and
#   runs the example ids on from AE-309; FE7 maps FG-13 to OD-4 and FG-14 to OD-5 and applies the rules of
#   profile 3, and for the kind repair requires that each of the bullets Options, Owner decision, Owner reason
#   and Channel is the fixed no-choice sentence "none: no design choice was open, because the finding names the
#   fix itself.". Profile 3 behaves exactly as before.
#   Profile 5 (--round 5), used by plans 04-18 and 04-19, differs from profile 4 in values and in the derived
#   number of changes, nothing more. --print-decision-questions prints the four decisions OD-6 to OD-9 (findings
#   RF-X-001, RF-X-002, RF-X-003 and RF-X-004, each with the options "Add examples" and "Say none needed") in the
#   form of profile 3, and --print-register-skeleton prints the skeleton of the fix register of round 5 with the
#   heading "## The changes", the changes whose primary finding has the disposition fix in the disposition record
#   of round 4 or its addendum, and the findings without a disposition. The data function holds a static table of
#   seven changes: FG-16 (RF-X-001 and RF-B-004), FG-17 (RF-X-002), FG-18 (RF-X-003) and FG-19 (RF-X-004) are an
#   owner decision, FG-20 (RF-C-001), FG-21 (RF-C-002) and FG-22 (RF-B-001) are a repair; the findings field of a
#   change is cut to the findings that have the disposition fix. Stage edits runs the addendum checks DA1 to DA5
#   first and then FE3 to FE7. FE3 expects the findings without a disposition to be 33 less the findings of the
#   addendum and does not look up a quoted sentence that the text of round 4 does not hold; FE5 expects as many
#   entries as the register skeleton prints, the Kind cell that the data function gives, example ids that run on
#   from AE-311 and, with --complete, the Findings cells equal to exactly the findings with the disposition fix
#   in the record and the addendum; FE7 maps FG-16 to OD-6, FG-17 to OD-7, FG-18 to OD-8 and FG-19 to OD-9 and
#   applies the rules of profile 4.
#   Profile 6 (--round 6), used by plans 04-22 and 04-23, is profile 5 one level up: values and a few constants
#   made profile variables, nothing else. The profile variables, set in the one profile block and read by the
#   code that profiles 5 and 6 share, are ADD_RND (the round of the review whose findings the addendum
#   dispositions: 4 in profile 5, 5 in profile 6; it names the round in the calls of the review check script that
#   print the disposition question and in the messages), DADD_PATH (the default of --addendum), NUNDISP_BASE (33,
#   21), AD_H1, AD_FOLLOWS_TEXT and AD_DEFAULT_IDS (RG-C-001,RG-X-001,RG-X-004), the id prefix (RG), the static
#   table of changes, the register heading and the register introduction. Profile 6 reads the approval record of
#   fix round 5 (so that the text approved before is the text of round 5), the disposition record and the review
#   note of round 5 and the addendum of round 5, finds the findings with the prefix RG, has up to three changes
#   FG-23 to FG-25 (FG-23 RG-A-001 and RG-X-004, repair; FG-24 RG-C-001, owner decision; FG-25 RG-X-001, owner
#   decision; a change is present only when its primary finding has the disposition fix in the record or the
#   addendum, with the findings field cut to those with that disposition, so the number of changes is derived),
#   and allows the stages edits, dispositions, approval-pending and approval-recorded (the stage defaults to edits;
#   the stages state and decisions and the printer of the decisions record exit 2). The approval stages and the
#   printers --print-delta, --print-approval-questions, --print-approval-packet and
#   --print-approval-record-skeleton work under --round 6 as under --round 5, with the profile values ADD_RND
#   and AP_ORD (the ordinal word of the review in the paragraph "What you are asked": a fifth time). --print-decision-questions prints the two decisions OD-10 (RG-C-001, options "Not closed" and "Not
#   closed, or done") and OD-11 (RG-X-001, options "Record its hash", "Always approve it" and "Say it openly") in
#   the form of profile 3, always, whatever the dispositions are; --print-register-skeleton prints the register of
#   round 6 with the heading "## The changes". Stage edits runs the addendum checks DA1 to DA5 first and then FE3
#   to FE7 with the values of profile 6: example ids run on from AE-321, FE7 maps FG-24 to OD-10 and FG-25 to
#   OD-11 and applies the rules of profile 4 (FG-23 is a repair).
#   Profile 7 (--round 7), used by plans 04-26 and 04-27, is profile 6 one level up and reads no addendum: every
#   disposition of round 6 is in the disposition record, so ADD_RND is 0 and DADD_PATH, AD_H1, AD_FOLLOWS_TEXT and
#   AD_DEFAULT_IDS are empty (the addendum checks DA1 to DA5, the stage dispositions, --print-addendum-skeleton and
#   --findings exit 2 or do not run under --round 7). The new constants are NOTE6_PATH, DREC6_PATH, BRIEF6_PATH,
#   FREG7_PATH, APK7_PATH, ARC7_PATH and NUNDISP7_BASE (9: the findings of the note of round 6 with an empty
#   Disposition cell). Profile 7 reads the approval record of fix round 6 (so that the text approved before is the
#   text of round 6), the disposition record and the review note of round 6, finds the findings with the prefix RH,
#   and has up to three changes FG-26 to FG-28 (FG-26 RH-C-001, owner decision; FG-27 RH-X-001, repair; FG-28
#   RH-X-002, owner decision; the number of changes is derived as in profile 6). Plan 04-26 allows the stage edits
#   only; the stages approval-pending and approval-recorded and the approval printers exit 2 until plan 04-27.
#   --print-decision-questions prints the two decisions OD-12 (RH-C-001, options "Close as failed" and "Allow
#   cancelled") and OD-13 (RH-X-002, options "Base revision only" and "Forbid editing it") in the form of profile 3,
#   always, whatever the dispositions are; --print-register-skeleton prints the register of round 7 with the heading
#   "## The changes". Stage edits runs FE3 to FE7 with the values of profile 7: example ids run on from AE-324,
#   FE7 maps FG-26 to OD-12 and FG-28 to OD-13 and applies the rules of profile 4 (FG-27 is a repair).
#
# The checks of the disposition addendum (profiles 5 and 6), DA1 to DA5, on --addendum, the records and the note; they do
# not read the specification: DA1 the addendum is valid UTF-8 without byte order mark, LF only with one final LF,
# without a tab or a fill marker, passes the self-containment scan (the hash-like tokens of its table are
# allowed), has the H1, exactly one line "- Owner disposition date:", the three H2 headings in order and the
# closing line last; DA2 the seven copied pin rows and the Reports SHA-256 equal the disposition record,
# the Reports SHA-256 equals the hash of the Reports section of the note, the note file, the record file and the
# blob of the record at HEAD are right and the three owner rows are filled; DA3 each block is a finding of the
# note without a disposition that the record does not hold, once, in table order, with the question that the review
# check script prints, one of fix, accept, defer, reject and a reason (for accept, defer and reject not "none
# given"), the default findings (four in profile 5, three in profile 6) are present, and every fix has a change in the static table; DA4 the reply
# details (the two fixed questions, the name equal to the row Dispositions given by, a valid calendar date equal to
# the date line and not earlier than the date of the disposition record, and a filled Owner reply row); DA5 the
# section What follows equals the fixed text and the closing line ends the addendum.
#
# Stage state: ST1 the approval record holds exactly one outcome line "- Owner approval: approved" and the pin
# rows Result blob (40 lowercase hexadecimal digits), Reviewed SHA-256 (64) and Line count (an integer), the
# disposition record holds the same three rows, and the values are equal. ST2 is a fact line and not a check:
# "STATE: ..." says whether the working file, the index and HEAD all hold the round-1 blob (all round-1 live
# checks apply) or not (the live checks that pin the round-1 text fail by design; use --replay-round-1).
#
# Stage decisions, on --decisions: FD1 valid UTF-8 without byte order mark, LF only with one final LF and no
# tab, no fill marker outside headings, no local path, web address, link, scratch or transcript word and no
# hash-like token except the round-1 result blob, the round-1 SHA-256 and the blob of the disposition record
# at HEAD; FD2 the structure (the H1, one line each of the two header lines, the four H2 headings in order,
# the seven H3 headings D-1 to D-5, Name and Date in order, the closing line last); FD3 the table of the text
# before the fix round equals the values of the two round-1 records and the blob of the disposition record at
# HEAD; FD4 the Question and Options bullets of each decision equal the printed ones character for character;
# FD5 each Answer is exactly one option label of its decision and each Owner reason is non-empty; FD6 the name
# is non-empty and equals the header line, the date is a valid calendar date (YYYY-MM-DD), equals the header
# line and is not earlier than the owner disposition date of the disposition record, and the two Answer lines
# of the reply details equal them; FD7 the What follows paragraph equals the printed one; FD8 the Findings
# line of each decision equals the printed one and names only findings with the disposition fix in the
# disposition record.
#
# Stage edits, on --spec and --register: the text of round 1 is read with git from the blob that the approval
# record names. A group counts as drafted when the Status cell of its row in the register reads drafted.
# FE1 for each drafted group the old statement is gone and the new facts are present in the places the group
# names, and its examples exist with their tags; FE2 the statements that stay true are unchanged (the sentence
# of Section 22.2 on the actions that can answer blocked, the last cell of every row of both tables of results,
# the realization row of the result blocked, the examples AE-259 and AE-287); FE3 minimality (the first eight
# lines, the quoted sentences of the 14 findings that were not dispositioned, the changed paths, every changed
# line inside a section that the register lists, no tab in an added line); FE4 every removed line that holds
# MUST, SHOULD or MAY is listed in the register with a reason; FE5 the register (layout, fields, quoted
# fragments, sections, examples, encoding, self-containment; with --complete all nine groups and the findings;
# the bullet Notes of an entry may be followed by nested bullets, one per result of the sweep for stale
# statements, and a bullet of the heading "Normative lines removed or reworded" has the form
# "- <first 60 characters of the removed line> :: <reason>", and one of the heading "Findings whose quoted
# sentence an edit touched" the form "- <finding id> :: <reason>");
# FE6 the Phase 2 check ends RESULT: PASS in --final mode on the specification under test.
#
# Stage approval-pending, on --identity, --packet, --register and --spec: AP1 the pins of the diff identity note
# equal those computed from the working specification (result blob, SHA-256, line count, diffstat, base blob),
# the working file, the index and HEAD hold one blob, the note is clean text and quotes RESULT: PASS; AP2 the
# packet, its status line read as the pending form, equals the output of --print-approval-packet byte for byte;
# AP3 the packet is clean text and passes the self-containment scan; AP4 the stage edits with --complete and the
# Phase 2 check with --final end RESULT: PASS; AP5 the status line is the pending form, or the recorded form
# when the record exists.
#
# Stage approval-recorded, on --record, --packet and --spec: AR1 the record is clean text, holds no fill marker,
# passes the scan and has the expected structure; AR2 the pin rows equal those computed from the live text and
# the pins of the packet, and the packet is the printed one; AR3 the Question bullets equal the printed
# questions; AR4 the answers and the outcome follow the rule; AR5 the name and the date are complete and
# consistent, and the date is not earlier than the disposition date of round 1.
#
# Output: one line per check, "PASS ID message" or "FAIL ID message"; "WARN ID message" lines and the
# "STATE:" lines are not counted; then "RESULT: PASS" or "RESULT: FAIL N". Exit 0 on pass, 1 on any failed
# check, 2 on a usage error or an unreadable input.
# Nothing is written outside a temporary directory that is removed on exit.

# The printf formats contain backticks on purpose: they are literal text of the printed records.
# The check functions of the groups are called by name; the fixed message texts hold backticks.
# shellcheck disable=SC2016,SC2329

set -u
export LC_ALL=C
export GIT_OPTIONAL_LOCKS=0
SELF="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
cd "$(git rev-parse --show-toplevel)" || { echo "not inside a git repository" >&2; exit 2; }
ROOT=$(pwd)

SPEC="docs/method/GG-SAD_normative_method_specification.md"
CHK=".planning/phases/04-independent-review/04-check-independent-review.sh"
CHK2=".planning/phases/02-normative-drafting/02-check-normative-diff.sh"
CHK3=".planning/phases/03-owner-approval/03-check-owner-approval.sh"
ARC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-owner-approval-record.md"
DREC_DEFAULT=".planning/reviews/2026-10-25-normative-spec-review-disposition-record.md"
NOTE_DEFAULT=".planning/reviews/2026-10-25-normative-spec-independent-review.md"
FREG_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-register.md"
FDEC_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-decisions.md"
PACKET_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-approval-packet.md"
RECORD_DEFAULT=".planning/reviews/2026-10-26-normative-spec-fix-round-approval-record.md"
IDENTITY_DEFAULT=".planning/reviews/2026-10-24-normative-spec-diff-identity.md"
FILL="@@FILL@@"
# The files of round 2 (the fix round that follows the first independent review), read by the profile 3 and by
# the replay of round 2.
ARC2_PATH=".planning/reviews/2026-10-26-normative-spec-fix-round-approval-record.md"
DREC2_PATH=".planning/reviews/2026-10-26-normative-spec-review-disposition-record-round-2.md"
NOTE2_PATH=".planning/reviews/2026-10-26-normative-spec-independent-review-round-2.md"
FREG2_PATH=".planning/reviews/2026-10-26-normative-spec-fix-round-register.md"
APK2_PATH=".planning/reviews/2026-10-26-normative-spec-fix-round-approval-packet.md"
BRIEF2_PATH=".planning/phases/04-independent-review/04-REVIEW-BRIEF-R2.md"
FREG3_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-3-register.md"
APK3_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-3-approval-packet.md"
ARC3_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-3-approval-record.md"
# The files of round 3 (the fix round that follows the second independent review), read by profile 4.
NOTE3_PATH=".planning/reviews/2026-10-27-normative-spec-independent-review-round-3.md"
DREC3_PATH=".planning/reviews/2026-10-27-normative-spec-review-disposition-record-round-3.md"
BRIEF3_PATH=".planning/phases/04-independent-review/04-REVIEW-BRIEF-R3.md"
# The files of round 4 (the fix round that follows the third independent review).
FREG4_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-4-register.md"
APK4_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-packet.md"
ARC4_PATH=".planning/reviews/2026-10-27-normative-spec-fix-round-4-approval-record.md"
NOTE4_PATH=".planning/reviews/2026-10-27-normative-spec-independent-review-round-4.md"
DREC4_PATH=".planning/reviews/2026-10-27-normative-spec-review-disposition-record-round-4.md"
BRIEF4_PATH=".planning/phases/04-independent-review/04-REVIEW-BRIEF-R4.md"
# The files of round 5 (the fix round that follows the fourth independent review): the disposition addendum of
# round 4 and the register, the packet and the record of fix round 5.
DADD4_PATH=".planning/reviews/2026-10-28-normative-spec-review-disposition-addendum-round-4.md"
FREG5_PATH=".planning/reviews/2026-10-28-normative-spec-fix-round-5-register.md"
APK5_PATH=".planning/reviews/2026-10-28-normative-spec-fix-round-5-approval-packet.md"
ARC5_PATH=".planning/reviews/2026-10-28-normative-spec-fix-round-5-approval-record.md"
# The number of findings of the review note of round 4 with an empty Disposition cell (34 rows, one dispositioned).
NUNDISP5_BASE=33
# The files of round 6 (the fix round that follows the fifth independent review): the review note, the disposition
# record and the disposition addendum of round 5, and the register, the packet and the record of
# fix round 6.
NOTE5_PATH=".planning/reviews/2026-10-28-normative-spec-independent-review-round-5.md"
DREC5_PATH=".planning/reviews/2026-10-28-normative-spec-review-disposition-record-round-5.md"
BRIEF5_PATH=".planning/phases/04-independent-review/04-REVIEW-BRIEF-R5.md"
DADD5_PATH=".planning/reviews/2026-10-29-normative-spec-review-disposition-addendum-round-5.md"
FREG6_PATH=".planning/reviews/2026-10-29-normative-spec-fix-round-6-register.md"
APK6_PATH=".planning/reviews/2026-10-29-normative-spec-fix-round-6-approval-packet.md"
ARC6_PATH=".planning/reviews/2026-10-29-normative-spec-fix-round-6-approval-record.md"
# The number of findings of the review note of round 5 with an empty Disposition cell (22 rows, one dispositioned).
NUNDISP6_BASE=21
# The files of round 7 (the fix round that follows the sixth independent review): the review note and the disposition
# record of round 6, and the register, the packet and the record of fix round 7. Round 7 has no
# disposition addendum.
NOTE6_PATH=".planning/reviews/2026-10-29-normative-spec-independent-review-round-6.md"
DREC6_PATH=".planning/reviews/2026-10-29-normative-spec-review-disposition-record-round-6.md"
FREG7_PATH=".planning/reviews/2026-10-30-normative-spec-fix-round-7-register.md"
APK7_PATH=".planning/reviews/2026-10-30-normative-spec-fix-round-7-approval-packet.md"
ARC7_PATH=".planning/reviews/2026-10-30-normative-spec-fix-round-7-approval-record.md"
# The number of findings of the review note of round 6 with an empty Disposition cell (12 rows, three dispositioned).
NUNDISP7_BASE=9
FIXP=".planning/phases/04-independent-review/04-check-fix-round.sh"

STAGE=""
APPROVAL=""
DISPO=""
DECISIONS="$FDEC_DEFAULT"
REGISTER=""
SPECFILE="$SPEC"
BASE="origin/main"
ROUND=2
REPLAY=0
RP1=0
RP2=0
RP3=0
RP4=0
RP5=0
ADDENDUM=""
PRINT_ADS=0
ADS_FINDINGS=""
CURRENT=0
PRINT_Q=0
PRINT_SKEL=0
PRINT_REG=0
COMPLETE=0
PACKET=""
RECORD=""
IDENTITY="$IDENTITY_DEFAULT"
PRINT_DELTA=0
PRINT_AQ=0
PRINT_APK=0
PRINT_ARS=0

usage() {
  awk 'NR > 1 && /^#/ { sub(/^# ?/, ""); print; next } NR > 1 { exit }' "$0"
}

need_value() {
  if [ "$#" -lt 2 ] || [ -z "$2" ]; then
    echo "option $1 needs a value" >&2
    exit 2
  fi
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --stage) need_value "$@"; STAGE="$2"; shift 2 ;;
    --approval-record) need_value "$@"; APPROVAL="$2"; shift 2 ;;
    --disposition-record) need_value "$@"; DISPO="$2"; shift 2 ;;
    --decisions) need_value "$@"; DECISIONS="$2"; shift 2 ;;
    --spec) need_value "$@"; SPECFILE="$2"; shift 2 ;;
    --register) need_value "$@"; REGISTER="$2"; shift 2 ;;
    --complete) COMPLETE=1; shift ;;
    --packet) need_value "$@"; PACKET="$2"; shift 2 ;;
    --record) need_value "$@"; RECORD="$2"; shift 2 ;;
    --identity) need_value "$@"; IDENTITY="$2"; shift 2 ;;
    --print-delta) PRINT_DELTA=1; shift ;;
    --print-approval-questions) PRINT_AQ=1; shift ;;
    --print-approval-packet) PRINT_APK=1; shift ;;
    --print-approval-record-skeleton) PRINT_ARS=1; shift ;;
    --base) need_value "$@"; BASE="$2"; shift 2 ;;
    --replay-round-1) REPLAY=1; RP1=1; shift ;;
    --replay-round-2) REPLAY=1; RP2=1; shift ;;
    --replay-round-3) REPLAY=1; RP3=1; shift ;;
    --replay-round-4) REPLAY=1; RP4=1; shift ;;
    --replay-round-5) REPLAY=1; RP5=1; shift ;;
    --addendum) need_value "$@"; ADDENDUM="$2"; shift 2 ;;
    --print-addendum-skeleton) PRINT_ADS=1; shift ;;
    --findings) need_value "$@"; ADS_FINDINGS="$2"; shift 2 ;;
    --round) need_value "$@"; ROUND="$2"; shift 2 ;;
    --with-current-scripts) CURRENT=1; shift ;;
    --print-decision-questions) PRINT_Q=1; shift ;;
    --print-decisions-skeleton) PRINT_SKEL=1; shift ;;
    --print-register-skeleton) PRINT_REG=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

case "$ROUND" in
  2|3|4|5|6|7) ;;
  *) echo "--round must be 2, 3, 4, 5, 6 or 7" >&2; exit 2 ;;
esac
[ "$RP1" -eq 0 ] || [ "$RP2" -eq 0 ] || { echo "--replay-round-1 and --replay-round-2 cannot be used together" >&2; exit 2; }
[ "$RP3" -eq 0 ] || { [ "$RP1" -eq 0 ] && [ "$RP2" -eq 0 ]; } || { echo "--replay-round-3 cannot be used with --replay-round-1 or --replay-round-2" >&2; exit 2; }
[ "$RP4" -eq 0 ] || { [ "$RP1" -eq 0 ] && [ "$RP2" -eq 0 ] && [ "$RP3" -eq 0 ]; } || { echo "--replay-round-4 cannot be used with --replay-round-1, --replay-round-2 or --replay-round-3" >&2; exit 2; }
[ "$RP5" -eq 0 ] || { [ "$RP1" -eq 0 ] && [ "$RP2" -eq 0 ] && [ "$RP3" -eq 0 ] && [ "$RP4" -eq 0 ]; } || { echo "--replay-round-5 cannot be used with --replay-round-1, --replay-round-2, --replay-round-3 or --replay-round-4" >&2; exit 2; }
if [ -z "$STAGE" ]; then
  if [ "$ROUND" -ge 3 ]; then STAGE="edits"; else STAGE="state"; fi
fi
case "$STAGE" in
  state|decisions|edits|approval-pending|approval-recorded|dispositions) ;;
  *) echo "--stage must be state, decisions, edits, approval-pending, approval-recorded or dispositions" >&2; exit 2 ;;
esac
[ "$STAGE" != dispositions ] || [ "$ROUND" -eq 5 ] || [ "$ROUND" -eq 6 ] || { echo "--stage dispositions is used with --round 5 or --round 6 only" >&2; exit 2; }
[ "$COMPLETE" -eq 0 ] || { [ "$STAGE" = edits ] && [ "$REPLAY" -eq 0 ]; } || { echo "--complete is used with --stage edits only" >&2; exit 2; }
[ "$CURRENT" -eq 0 ] || [ "$REPLAY" -eq 1 ] || { echo "--with-current-scripts is used with --replay-round-1, --replay-round-2, --replay-round-3, --replay-round-4 or --replay-round-5 only" >&2; exit 2; }
[ "$PRINT_ADS" -eq 0 ] || [ "$ROUND" -eq 5 ] || [ "$ROUND" -eq 6 ] || { echo "--print-addendum-skeleton is used with --round 5 or --round 6 only" >&2; exit 2; }
[ -z "$ADS_FINDINGS" ] || [ "$PRINT_ADS" -eq 1 ] || { echo "--findings is used with --print-addendum-skeleton only" >&2; exit 2; }
if [ "$ROUND" -eq 3 ]; then
  case "$STAGE" in
    edits|approval-pending|approval-recorded) ;;
    *) echo "--round 3 allows --stage edits, approval-pending or approval-recorded only" >&2; exit 2 ;;
  esac
fi
if [ "$ROUND" -eq 4 ]; then
  case "$STAGE" in
    edits|approval-pending|approval-recorded) ;;
    *) echo "--round 4 allows --stage edits, approval-pending or approval-recorded only" >&2; exit 2 ;;
  esac
fi
if [ "$ROUND" -eq 5 ]; then
  case "$STAGE" in
    edits|dispositions|approval-pending|approval-recorded) ;;
    *) echo "--round 5 allows --stage edits, dispositions, approval-pending or approval-recorded only" >&2; exit 2 ;;
  esac
fi
if [ "$ROUND" -eq 6 ]; then
  case "$STAGE" in
    edits|dispositions|approval-pending|approval-recorded) ;;
    *) echo "--round 6 allows --stage edits, dispositions, approval-pending or approval-recorded only" >&2; exit 2 ;;
  esac
fi
if [ "$ROUND" -eq 7 ]; then
  if [ "$STAGE" != edits ]; then
    echo "--round 7 allows --stage edits only" >&2
    exit 2
  fi
  if [ "$PRINT_DELTA" -eq 1 ] || [ "$PRINT_AQ" -eq 1 ] || [ "$PRINT_APK" -eq 1 ] || [ "$PRINT_ARS" -eq 1 ]; then
    echo "--round 7 has no approval printers yet" >&2
    exit 2
  fi
fi
if [ "$ROUND" -ge 3 ]; then
  [ "$RP1" -eq 0 ] || { echo "--replay-round-1 is used with --round 2 only" >&2; exit 2; }
  if [ "$PRINT_SKEL" -eq 1 ]; then
    echo "--round $ROUND has no decisions record" >&2
    exit 2
  fi
fi

# The round profile: the one place that sets every value that differs between round 2 (the default, the values this
# script has always held), round 3, round 4, round 5, round 6 and round 7. The profile variables of the disposition
# addendum (profiles 5 and 6; profile 7 has none and leaves them empty) are ADD_RND (the round of the review whose
# findings the addendum dispositions, 0 when the profile reads no addendum), DADD_PATH, NUNDISP_BASE, AD_H1,
# AD_FOLLOWS_TEXT and AD_DEFAULT_IDS.
ADD_RND=0
AP_ORD=""
DADD_PATH=""
NUNDISP_BASE=0
AD_H1=""
AD_FOLLOWS_TEXT=""
AD_DEFAULT_IDS=""
if [ "$ROUND" -ge 3 ]; then
  NCHG=3
  NCHG_W="three"
  REG_TBL_H="## The three changes"
  REG_BULLETS=("What changed" "Why" "Options" "Owner decision" "Owner reason" "Channel" "Before" "After" "Notes")
  if [ "$ROUND" -eq 3 ]; then
    ARC_DEFAULT="$ARC2_PATH"
    DREC_DEFAULT="$DREC2_PATH"
    NOTE_DEFAULT="$NOTE2_PATH"
    FREG_DEFAULT="$FREG3_PATH"
    FPFX="RR"
    NUNDISP=9
    EX_FIRST=306
    PACKET_DEFAULT="$APK3_PATH"
    RECORD_DEFAULT="$ARC3_PATH"
  elif [ "$ROUND" -eq 4 ]; then
    ARC_DEFAULT="$ARC3_PATH"
    DREC_DEFAULT="$DREC3_PATH"
    NOTE_DEFAULT="$NOTE3_PATH"
    FREG_DEFAULT="$FREG4_PATH"
    FPFX="RT"
    NUNDISP=20
    EX_FIRST=309
    PACKET_DEFAULT="$APK4_PATH"
    RECORD_DEFAULT="$ARC4_PATH"
  elif [ "$ROUND" -eq 5 ]; then
    # Profile 5: the number of changes depends on the dispositions and is derived once the records are read.
    ARC_DEFAULT="$ARC4_PATH"
    DREC_DEFAULT="$DREC4_PATH"
    NOTE_DEFAULT="$NOTE4_PATH"
    FREG_DEFAULT="$FREG5_PATH"
    FPFX="RF"
    NCHG=0
    NCHG_W="zero"
    NUNDISP=$NUNDISP5_BASE
    NUNDISP_BASE=$NUNDISP5_BASE
    EX_FIRST=311
    REG_TBL_H="## The changes"
    PACKET_DEFAULT="$APK5_PATH"
    RECORD_DEFAULT="$ARC5_PATH"
    ADD_RND=4
    AP_ORD="a fourth time"
    DADD_PATH="$DADD4_PATH"
    AD_H1='# Review disposition addendum, round 4: proposed normative method specification'
    AD_FOLLOWS_TEXT='The owner answered the findings above. A finding with the disposition fix is fixed in fix round 5 and listed in the register of that round; a finding with another disposition needs no change of the text. This addendum supplements the disposition record of round 4, which stays as it is.'
    AD_DEFAULT_IDS="RF-B-004,RF-X-002,RF-X-003,RF-X-004"
    [ -n "$ADDENDUM" ] || ADDENDUM="$DADD_PATH"
  elif [ "$ROUND" -eq 6 ]; then
    # Profile 6: profile 5 one level up. The text approved before is the text of round 5 (the approval record of fix
    # round 5), the number of changes is derived, and the addendum dispositions findings of the review of round 5.
    ARC_DEFAULT="$ARC5_PATH"
    DREC_DEFAULT="$DREC5_PATH"
    NOTE_DEFAULT="$NOTE5_PATH"
    FREG_DEFAULT="$FREG6_PATH"
    FPFX="RG"
    NCHG=0
    NCHG_W="zero"
    NUNDISP=$NUNDISP6_BASE
    NUNDISP_BASE=$NUNDISP6_BASE
    EX_FIRST=321
    REG_TBL_H="## The changes"
    PACKET_DEFAULT="$APK6_PATH"
    RECORD_DEFAULT="$ARC6_PATH"
    ADD_RND=5
    AP_ORD="a fifth time"
    DADD_PATH="$DADD5_PATH"
    AD_H1='# Review disposition addendum, round 5: proposed normative method specification'
    AD_FOLLOWS_TEXT='The owner answered the findings above. A finding with the disposition fix is fixed in fix round 6 and listed in the register of that round; a finding with another disposition needs no change of the text. This addendum supplements the disposition record of round 5, which stays as it is.'
    AD_DEFAULT_IDS="RG-C-001,RG-X-001,RG-X-004"
    [ -n "$ADDENDUM" ] || ADDENDUM="$DADD_PATH"
  else
    # Profile 7: profile 6 one level up, without an addendum (every disposition of round 6 is in the disposition
    # record). The text approved before is the text of round 6 (the approval record of fix round 6), the number of
    # changes is derived, ADD_RND is 0 and no addendum is read.
    ARC_DEFAULT="$ARC6_PATH"
    DREC_DEFAULT="$DREC6_PATH"
    NOTE_DEFAULT="$NOTE6_PATH"
    FREG_DEFAULT="$FREG7_PATH"
    FPFX="RH"
    NCHG=0
    NCHG_W="zero"
    NUNDISP=$NUNDISP7_BASE
    NUNDISP_BASE=$NUNDISP7_BASE
    EX_FIRST=324
    REG_TBL_H="## The changes"
    PACKET_DEFAULT="$APK7_PATH"
    RECORD_DEFAULT="$ARC7_PATH"
    ADD_RND=0
    AP_ORD="a sixth time"
    ADDENDUM=""
  fi
else
  FPFX="RV"
  NCHG=9
  NCHG_W="nine"
  NUNDISP=14
  EX_FIRST=295
  REG_TBL_H="## The nine changes"
  REG_BULLETS=("What changed" "Why" "My choice" "Before" "After" "Notes")
fi
REG_BULLETS_RE=$(printf '%s|' "${REG_BULLETS[@]}")
REG_BULLETS_RE=${REG_BULLETS_RE%|}
if [ -z "$APPROVAL" ]; then
  if [ "$RP2" -eq 1 ]; then APPROVAL="$ARC2_PATH"; elif [ "$RP3" -eq 1 ]; then APPROVAL="$ARC3_PATH"; elif [ "$RP4" -eq 1 ]; then APPROVAL="$ARC4_PATH"; elif [ "$RP5" -eq 1 ]; then APPROVAL="$ARC5_PATH"; else APPROVAL="$ARC_DEFAULT"; fi
fi
[ -n "$DISPO" ] || DISPO="$DREC_DEFAULT"
[ -n "$REGISTER" ] || REGISTER="$FREG_DEFAULT"
[ -n "$PACKET" ] || PACKET="$PACKET_DEFAULT"
[ -n "$RECORD" ] || RECORD="$RECORD_DEFAULT"

# decision_data: the fixed texts of the five decisions. One record per line, fields separated by a vertical
# bar: "D|id|header|findings" opens a decision, "Q|question" is its question, "O|label|description" is one
# option. No option is recommended; every description has the parts what happens, Gain and Cost.
decision_data() {
  cat << 'DATA'
D|D-1|Reopen pause|RV-A-001, RV-X-002
Q|Section 8.3 says that `reopen` (full profile) waits when the Definition of Wait of the new corrective scope determines a pause. The table of results in the same section says that `reopen` never answers `blocked`, and Section 22.2 lets only the actions that complete a change or a phase, and `resume`, answer `blocked`, so the result of a paused reopen is not determined. The first approval accepted the drafting choice that `reopen` is never blocked. What does a `reopen` answer when the Definition of Wait of its new scope determines a pause?
O|Rejected|nothing is written, `changed` is false and the change stays closed; the request is repeated when the condition is resolved. Gain: the smallest edit, consistent with the accepted drafting choice and with Section 22.2. Cost: the pause itself is not recorded and attempts cannot be counted.
O|Success, then waiting|the reopen takes effect and answers `success`, and the change returns to the resume phase with the status `waiting`. Gain: keeps the intent of the earlier wording of the row, Section 22.2 stays as it is, and the accepted drafting choice that `reopen` never answers `blocked` stays. Cost: a successful action can end in a wait, and the row of the transition table and the sentence after the table of results change.
O|Blocked|the evaluation is recorded, the change stays closed and the result is `blocked` with `changed` true. Gain: attempts become countable, as for `complete` and `resume`. Cost: the largest edit, because the row, the table of results, Section 22.2 and the realization row of the result `blocked` then name `reopen`, and it changes the accepted drafting choice.
D|D-2|Unevaluable gate|RV-A-003
Q|Section 24.2 settles `start` when a gate cannot be evaluated: `start` is rejected and no wait is created. For the other actions that evaluate gates and never answer `blocked` (in the full profile `wait`, `fail`, `cancel`, `supersede` and `reopen`; in the core profile `cancel` and `supersede`, which look for an active hard failure) the result is not stated: Section 24.2 says that the change waits, but a wait is a recorded change that these actions cannot answer under Section 22.2. What do these actions answer when a gate that applies to them cannot be evaluated?
O|Rejected|each of these actions is rejected with `changed` false, nothing is written and no wait is created, as for `start`. Gain: one rule for all of them, no new case of the result `blocked`, and Section 22.2 stays as it is. Cost: a `cancel` or `supersede` cannot proceed while a failure gate it must evaluate cannot be evaluated, and the failed evaluation is not recorded.
O|Cancel proceeds, others rejected|`cancel` and `supersede` take effect and the `not_evaluable` result is recorded, because a gate that cannot be evaluated is never a failure, while `wait`, `fail` and `reopen` are rejected with `changed` false, nothing written and no wait created. Gain: an authorized cancellation is never held up, and Section 22.2 stays as it is. Cost: a hard failure behind a gate that cannot be evaluated is not decided when the change is cancelled or superseded, two rules apply to these actions instead of one, and Section 8.4 and the `cancel` row of Section 23.4 get a clause.
O|Blocked|these actions answer `blocked`: the evaluation is recorded, the change waits as Section 24.2 says and the requested transition does not occur. Gain: the failed evaluation is recorded and attempts are countable, and rule 2 of Section 24.2 applies to every action alike. Cost: the largest edit, because Section 22.2, both tables of results and the realization row of the result `blocked` change, and a `cancel` can leave the change waiting instead of closing it.
D|D-3|Retry limit|RV-B-005
Q|The base text lists exceeding retry limits among the conditions that must terminate the flow. The specification makes a retry limit a soft fail condition: when it is reached the change pauses for a human, who closes it as failed or records a bounded override, and a retry limit that declares the severity hard is invalid. This was a drafting choice accepted in the first approval, and no owner decision speaks to it. Which severity may a retry limit have?
O|Soft, stated openly|a retry limit stays a soft fail condition as accepted; Section 12, where the obligation to terminate is limited, states that reaching a retry limit pauses the flow for a human disposition and that the flow ends as failed unless a human records an override. Gain: wording only, and the accepted drafting choice and the examples stay. Cost: the relaxation of the base text stays, and a reviewer may report it again for the owner's disposition.
O|Author's choice|a retry limit declares the severity hard or soft like any other fail condition; reaching a hard retry limit closes the change as failed, reaching a soft one pauses it. Gain: one rule for all fail conditions, and a project can choose termination without human action. Cost: the rule that a hard retry limit is invalid is removed, some examples change, and the accepted drafting choice changes.
O|Hard only|a retry limit is always a hard fail condition as in the base text; reaching it closes the change as failed without human action, no override applies to it, and a retry limit that declares soft is invalid. Gain: agrees with the base text, so there is no relaxation to state. Cost: it reverses the accepted drafting choice, a retry limit can no longer pause the flow for a human, and several examples change.
D|D-4|Text or binary|RV-E-001
Q|Section 25.2 hashes a text file after line-ending normalisation and a binary file byte for byte, but leaves the decision between text and binary to the implementation and only recommends (SHOULD) that a file is text when its bytes are valid UTF-8 and hold no zero byte. A content hash is therefore comparable only with one computed with the same decision. This was a drafting choice accepted in the first approval. How is the decision made?
O|One rule that must be followed|the recommended rule becomes a requirement (MUST): a file is text exactly when its bytes are valid UTF-8 and hold no zero byte, and binary otherwise. Gain: every conforming implementation computes the same hash for the same bytes, a hash computed by one implementation can be compared with one computed by another, and the edit is small. Cost: a binary format that happens to be valid UTF-8 without a zero byte is treated as text.
O|Recorded with the hash|the implementation keeps its own rule, but every stored content hash of a file is recorded with the kind that was applied (text or binary) and is verified with that kind. Gain: implementations keep their own classification, and a verification always uses the kind that was recorded. Cost: the larger edit, because the definition of the entry of the state document (Section 25.1), the approval and frozen gate records and the examples that show stored hashes change, and two implementations can record different kinds for the same bytes.
D|D-5|Verify-only CI|RV-X-003
Q|Owner decisions O-2 and O-11 bring continuous integration into scope as verify-only: CI checks history integrity and the anchor, that the frozen gates match the approval, that approvals are current and at the required level, and the scope against the base, and that no hard failure is active, and it does not execute the change's own commands with CI's privileges; CI proves the record, not the outcome. The specification names a read-only action `guard` in Sections 22.1 and 23.4 but never says what it checks, and has no other text for this decision. What should the specification carry?
O|Define guard as the verify-only action|a new subsection of Section 22 defines `guard`: read-only in both profiles, the five verifications of the decision, no execution of any command that the change or the project defines, `success` when all hold and `rejected` with issues otherwise, with acceptance examples; running `guard` in a pipeline is the CI integration, and an on-demand guard that enforces hard failures is met by the caller acting on the result. Gain: the decision has normative text, and the later workflow phase has specification text for its CI check. Cost: new normative text, issue codes and examples to be approved and reviewed, in which the Requestor's own drafting readings (listed for the owner at the approval) go beyond the decision.
O|Carry no CI text|the name `guard` is removed from Sections 22.1 and 23.4 and the specification states nothing about CI. Gain: the smallest edit, and no new normative text to approve or review. Cost: the decision has no normative text, which differs from decisions O-1 to O-10, and the later workflow phase has no specification text for its CI check.
DATA
}

NAME_Q='Under which name or handle should these decisions be recorded for the repository owner?'
DATE_Q='Which date are these decisions given? Give it as YYYY-MM-DD.'
H1_LINE='# Fix round decisions: proposed normative method specification'
FOLLOWS_TEXT='The decisions bind the drafting of plans 04-06 and 04-07; every other fix is drafted as a reading of the existing text that the owner sees in the approval packet and may change; the specification is edited only in those plans, and a new owner approval and a new independent review follow; this record is the record of these decisions only.'
CLOSING_LINE='This record is evidence only. It does not change the reviewed file.'
DEC_IDS=(D-1 D-2 D-3 D-4 D-5)

# print_questions: the five decisions as the owner is asked them.
print_questions() {
  local tag a b c first=1
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D) if [ "$first" -eq 0 ]; then printf '\n'; fi; first=0; printf '%s %s\nFindings: %s\n' "$a" "$b" "$c" ;;
      Q) printf '%s\n' "$a" ;;
      O) printf -- '- %s: %s\n' "$a" "$b" ;;
    esac
  done < <(decision_data)
}

# dec_header ID, dec_findings ID, dec_labels ID: parts of one decision.
dec_header() {
  local tag a b c
  while IFS='|' read -r tag a b c; do
    if [ "$tag" = D ] && [ "$a" = "$1" ]; then printf '%s\n' "$b"; return 0; fi
  done < <(decision_data)
}
dec_findings() {
  local tag a b c
  while IFS='|' read -r tag a b c; do
    if [ "$tag" = D ] && [ "$a" = "$1" ]; then printf '%s\n' "$c"; return 0; fi
  done < <(decision_data)
}
dec_labels() {
  local tag a b c cur=""
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D) cur=$a ;;
      O) if [ "$cur" = "$1" ]; then printf '%s\n' "$a"; fi ;;
    esac
  done < <(decision_data)
}

if [ "$PRINT_Q" -eq 1 ] && [ "$ROUND" -eq 2 ]; then
  print_questions
  exit 0
fi

TMP=$(mktemp -d) || { echo "cannot create a temporary directory" >&2; exit 2; }
trap 'rm -rf "$TMP"' EXIT
AR="$TMP/arc"
DR="$TMP/dispo"
DC="$TMP/decisions"
SP="$TMP/spec"
NT="$TMP/note"
RG="$TMP/register"
T1="$TMP/text1"
PK="$TMP/packet"
ID="$TMP/identity"
RC="$TMP/record"

readable() {
  if [ -f "$2" ] && [ -r "$2" ] && cp "$2" "$1" 2> /dev/null; then
    return 0
  fi
  echo "cannot read $2" >&2
  exit 2
}

git rev-parse --verify --quiet "$BASE^{commit}" > /dev/null || { echo "--base $BASE is not a commit" >&2; exit 2; }
readable "$AR" "$APPROVAL"
readable "$DR" "$DISPO"
if [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = decisions ]; then readable "$DC" "$DECISIONS"; fi
if [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = state ]; then readable "$SP" "$SPECFILE"; fi
if [ "$PRINT_REG" -eq 1 ] || [ "$PRINT_Q" -eq 1 ] || [ "$PRINT_ADS" -eq 1 ] || { [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && { [ "$STAGE" = edits ] || [ "$STAGE" = dispositions ]; }; }; then readable "$NT" "$NOTE_DEFAULT"; fi
if [ "$PRINT_REG" -eq 0 ] && [ "$PRINT_Q" -eq 0 ] && [ "$PRINT_ADS" -eq 0 ] && [ "$PRINT_SKEL" -eq 0 ] && [ "$REPLAY" -eq 0 ] && [ "$STAGE" = edits ]; then
  readable "$SP" "$SPECFILE"
  readable "$RG" "$REGISTER"
fi
AP_ON=0
if [ "$REPLAY" -eq 0 ] && [ "$PRINT_REG" -eq 0 ] && [ "$PRINT_SKEL" -eq 0 ]; then
  if [ "$PRINT_DELTA" -eq 1 ] || [ "$PRINT_AQ" -eq 1 ] || [ "$PRINT_APK" -eq 1 ] || [ "$PRINT_ARS" -eq 1 ] \
    || [ "$STAGE" = approval-pending ] || [ "$STAGE" = approval-recorded ]; then
    AP_ON=1
  fi
fi
if [ "$AP_ON" -eq 1 ]; then
  if [ "$STAGE" != edits ]; then
    readable "$SP" "$SPECFILE"
    readable "$RG" "$REGISTER"
  fi
  if [ "$PRINT_ARS" -eq 1 ] || [ "$STAGE" = approval-pending ] || [ "$STAGE" = approval-recorded ]; then readable "$PK" "$PACKET"; fi
  if [ "$STAGE" = approval-pending ]; then readable "$ID" "$IDENTITY"; fi
  if [ "$STAGE" = approval-recorded ]; then readable "$RC" "$RECORD"; fi
fi

FAILS=0
pass() { echo "PASS $1 $2"; }
fail() { echo "FAIL $1 $2"; FAILS=$((FAILS + 1)); }

finish() {
  if [ "$FAILS" -eq 0 ]; then echo "RESULT: PASS"; exit 0; fi
  echo "RESULT: FAIL $FAILS"
  exit 1
}

# enc1 FILE: print the problem with the encoding of FILE, nothing when it is valid UTF-8 without BOM.
enc1() {
  local bom
  bom=$(head -c3 "$1" | od -An -tx1 | tr -d ' \n')
  if [ "$bom" = efbbbf ]; then
    echo "file starts with a UTF-8 byte order mark"
  elif ! iconv -f UTF-8 -t UTF-8 "$1" > /dev/null 2>&1; then
    echo "file is not valid UTF-8"
  fi
}

# enc2 FILE: print the problem with the line endings of FILE, nothing when LF only with one final LF,
# no trailing blank line and no tab.
enc2() {
  if [ "$(tr -cd '\r' < "$1" | wc -c)" -gt 0 ]; then
    echo "CR byte found (first at line $(tr '\r' '\001' < "$1" | grep -n -m1 -a $'\001' | cut -d: -f1)); LF only is allowed"
  elif [ ! -s "$1" ]; then
    echo "file is empty"
  elif [ "$(tail -c1 "$1" | od -An -tx1 | tr -d ' \n')" != 0a ]; then
    echo "file does not end with a line feed"
  elif ! tail -n1 "$1" | grep -q '[^[:space:]]'; then
    echo "file ends with a blank line"
  elif [ "$(tr -cd '\t' < "$1" | wc -c)" -gt 0 ]; then
    echo "tab character found (first at line $(tr '\t' '\001' < "$1" | grep -n -m1 -a $'\001' | cut -d: -f1))"
  fi
}

# parse_pins FILE OUT: write one line "label TAB raw cell TAB first backticked token" for every table row of
# FILE before its first H2 heading.
parse_pins() {
  awk '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    /^## / { exit }
    /^\| / && $0 !~ /^\|[-| ]+\|$/ {
      n = split($0, c, "|")
      label = trim(c[2]); raw = trim(c[3]); tok = ""
      if (match(raw, /`[^`]*`/)) tok = substr(raw, RSTART + 1, RLENGTH - 2)
      if (label != "Field") print label "\t" raw "\t" tok
    }
  ' "$1" > "$2"
}
pin_count() { awk -F'\t' -v l="$2" '$1 == l { n++ } END { print n + 0 }' "$1"; }
pin_tok() { awk -F'\t' -v l="$2" '$1 == l { print $3; exit }' "$1"; }
pin_raw() { awk -F'\t' -v l="$2" '$1 == l { print $2; exit }' "$1"; }

parse_pins "$AR" "$TMP/arc.pins"
parse_pins "$DR" "$TMP/dr.pins"
A_BLOB=$(pin_tok "$TMP/arc.pins" "Result blob")
A_SHA=$(pin_tok "$TMP/arc.pins" "Reviewed SHA-256")
A_LINES=$(pin_tok "$TMP/arc.pins" "Line count")
D_BLOB=$(pin_tok "$TMP/dr.pins" "Result blob")
D_SHA=$(pin_tok "$TMP/dr.pins" "Reviewed SHA-256")
D_LINES=$(pin_tok "$TMP/dr.pins" "Line count")

# drec_fix_ids: the finding ids with the disposition fix in the disposition record, one per line.
drec_fix_ids() {
  awk -v p="$FPFX-" '/^### / { id = (index($2, p) == 1) ? $2 : "" } /^- Disposition: fix$/ && id != "" { print id; id = "" }' "$DR"
  if [ "$ROUND" -ge 5 ]; then
    awk -v p="$FPFX-" '/^### / { id = (index($2, p) == 1) ? $2 : "" } /^- Disposition: fix$/ && id != "" { print id; id = "" }' "$AD"
  fi
}

# add_ids: the finding ids of the blocks of the disposition addendum (profile 5), one per line in file order.
add_ids() {
  awk -v p="$FPFX-" '/^### / && index($2, p) == 1 { print $2 }' "$AD"
}

# print_skeleton: the decisions record with the fill marker in every field the owner completes.
print_skeleton() {
  local drb tag a b c cur="" n_fix
  drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || { echo "cannot read the disposition record at HEAD" >&2; exit 2; }
  n_fix=$(drec_fix_ids | wc -l | tr -d ' ')
  printf '%s\n\n' "$H1_LINE"
  printf -- '- Decisions given by: %s\n- Owner decision date: %s\n\n' "$FILL" "$FILL"
  printf '## The text before the fix round\n\n| Field | Value |\n|---|---|\n'
  printf '| Reviewed file | %s |\n' "$(pin_raw "$TMP/arc.pins" "Reviewed file")"
  printf '| Round-1 result blob | %s |\n' "$(pin_raw "$TMP/arc.pins" "Result blob")"
  printf '| Round-1 reviewed SHA-256 | %s |\n' "$(pin_raw "$TMP/arc.pins" "Reviewed SHA-256")"
  printf '| Round-1 line count | %s |\n' "$(pin_raw "$TMP/arc.pins" "Line count")"
  printf '| Round-1 disposition record file | `%s` |\n' "$DREC_DEFAULT"
  printf '| Round-1 disposition record blob | `%s` |\n' "$drb"
  printf '| Findings dispositioned fix | `%s` |\n\n' "$n_fix"
  printf '## Decisions\n\n'
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D)
        if [ -n "$cur" ]; then printf -- '- Answer: %s\n- Owner reason: %s\n\n' "$FILL" "$FILL"; fi
        cur=$a
        printf '### %s — %s\n\n- Findings: %s\n' "$a" "$b" "$c" ;;
      Q) printf -- '- Question: %s\n- Options:\n' "$a" ;;
      O) printf '  - %s: %s\n' "$a" "$b" ;;
    esac
  done < <(decision_data)
  printf -- '- Answer: %s\n- Owner reason: %s\n\n' "$FILL" "$FILL"
  printf '## Reply details\n\n### Name\n\n- Question: %s\n- Answer: %s\n\n### Date\n\n- Question: %s\n- Answer: %s\n\n' "$NAME_Q" "$FILL" "$DATE_Q" "$FILL"
  printf '## What follows\n\n%s\n\n%s\n' "$FOLLOWS_TEXT" "$CLOSING_LINE"
}

# ---- the fix register: data and printer ------------------------------------------------------------------

REG_H1='# Fix register: what changed in the specification and why'
REG_INTRO='This register lists the nine changes made to the specification to fix the eleven findings of the first independent review. A change is a repair when the text had one consistent reading, and my choice when more than one reading was possible; for a choice the other readings are named, so that the owner can pick another one. A choice is a proposal: it becomes the decision of the owner only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG_HEADER='The header of the specification (the Version line and the Revision line) is unchanged by this round.'
REG3_H1='# Fix register, round 3: what changed in the specification and why'
REG3_INTRO='This register lists the three changes made to the specification to fix the three BLOCKING findings of the second independent review that the owner dispositioned fix. Each change implements the way the owner chose, which is recorded in the entry together with the options that were offered. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG4_H1='# Fix register, round 4: what changed in the specification and why'
REG4_INTRO='This register lists the three changes made to the specification to fix the three BLOCKING findings of the third independent review that the owner dispositioned fix. For two of them the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For the third the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG5_H1='# Fix register, round 5: what changed in the specification and why'
REG5_INTRO='This register lists the changes made to the specification to fix the BLOCKING finding of the fourth independent review that the owner dispositioned fix, and the related findings that the owner dispositioned fix in the disposition addendum of round 4. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG6_H1='# Fix register, round 6: what changed in the specification and why'
REG6_INTRO='This register lists the changes made to the specification to fix the BLOCKING finding of the fifth independent review that the owner dispositioned fix, and the further findings that the owner dispositioned fix in the disposition addendum of round 5. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.'
REG7_H1='# Fix register, round 7: what changed in the specification and why'
REG7_INTRO='This register lists the three changes made to the specification to fix the three BLOCKING findings of the sixth independent review that the owner dispositioned fix. For a change of the kind owner decision the finding leaves more than one way to fix, and the change implements the way the owner chose, which is recorded in the entry together with the options that were offered. For a change of the kind repair the finding names the fix itself, and its entry says that no design choice was open. A choice becomes final only through the owner approval of the exact new text. The approval packet is printed from this register.'
CHANNEL_TEXT='Given by the repository owner through the interactive question tool and relayed by the orchestrating session.'
NOCHOICE_TEXT='none: no design choice was open, because the finding names the fix itself.'

# fg5_static: the static table of the seven changes of profile 5, "id|title|findings|kind". The first finding of a
# row is its primary finding.
fg5_static() {
  if [ "$ROUND" -eq 7 ]; then
    cat << 'DATA7'
FG-26|How cancel and supersede end a change that waits for a decision on a soft failure|RH-C-001|owner decision
FG-27|The first entry of a change that was converted from a YAML state document|RH-X-001|repair
FG-28|Which revision of an ignore file the scope measurement applies|RH-X-002|owner decision
DATA7
    return 0
  fi
  if [ "$ROUND" -eq 6 ]; then
    cat << 'DATA6'
FG-23|A reserved device name that is followed by an extension|RG-A-001, RG-X-004|repair
FG-24|Which change a supersede action may name as its replacement|RG-C-001|owner decision
FG-25|A specification file that nothing protects when its approval is never required|RG-X-001|owner decision
DATA6
    return 0
  fi
  cat << 'DATA5'
FG-16|Rules of the full-only templates that have no acceptance example|RF-X-001, RF-B-004|owner decision
FG-17|Rules on ADR conflicts, drift and breaking changes that have no acceptance example|RF-X-002|owner decision
FG-18|Rules on the review cycle and its artifacts that have no acceptance example|RF-X-003|owner decision
FG-19|Prohibitions on an AI agent that have no acceptance example|RF-X-004|owner decision
FG-20|How the evaluation of a core change stops|RF-C-001|repair
FG-21|A retry limit that names a check gate which does not exist|RF-C-002|repair
FG-22|A sentence that cites the earlier text of the method|RF-B-001|repair
DATA5
}

# fg5_ids: every finding id that the static table of profile 5 names (primary or companion), one per line.
fg5_ids() {
  fg5_static | cut -d'|' -f3 | tr ',' '\n' | tr -d ' '
}

# fg5_data: the rows of the static table whose primary finding has the disposition fix in the disposition record or
# the addendum, with the findings field cut to the findings that have it.
fg5_data() {
  local fixids g t f k prim x cutf
  fixids=$(drec_fix_ids)
  while IFS='|' read -r g t f k; do
    prim=${f%%,*}
    printf '%s\n' "$fixids" | grep -q -x -F -e "$prim" || continue
    cutf=""
    for x in ${f//,/ }; do
      if printf '%s\n' "$fixids" | grep -q -x -F -e "$x"; then cutf="${cutf:+$cutf, }$x"; fi
    done
    printf '%s|%s|%s|%s\n' "$g" "$t" "$cutf" "$k"
  done < <(fg5_static)
}

# fg_data: one line per group, "id|title|findings|kind".
fg_data() {
  if [ "$ROUND" -ge 5 ]; then
    fg5_data
    return 0
  fi
  if [ "$ROUND" -eq 4 ]; then
    cat << 'DATA4'
FG-13|How the gate comparison treats the supersede action|RT-A-001|owner decision
FG-14|What happens when a retry limit is reached|RT-B-001|owner decision
FG-15|An example for a wait, a fail or a reopen that cannot be evaluated|RT-D-001|repair
DATA4
    return 0
  fi
  if [ "$ROUND" -eq 3 ]; then
    cat << 'DATA3'
FG-10|How the guard check treats an equivalent to the history anchor|RR-B-001|owner decision
FG-11|How the scope check treats ignore settings|RR-X-001|owner decision
FG-12|When the fail action is allowed in the full profile|RR-X-002|owner decision
DATA3
    return 0
  fi
  cat << 'DATA'
FG-01|A pause request on a change that has already hit a hard failure|RV-A-002, RV-X-001|repair
FG-02|Re-opening a closed change when its new work would have to wait|RV-A-001, RV-X-002|my choice
FG-03|Starting a change when a check cannot be run|RV-C-001, RV-A-003|repair
FG-04|Cancelling or replacing a change when a check cannot be run|RV-A-003|my choice
FG-05|Which rule decides when a ready condition is not met|RV-D-001|repair
FG-06|Recording a question in the full profile|RV-B-001|repair
FG-07|What happens when a retry limit is reached|RV-B-005|my choice
FG-08|Deciding whether a file is text or binary before hashing it|RV-E-001|my choice
FG-09|The guard check for continuous integration|RV-X-003|my choice
DATA
}

# fg_kind ID: the kind of the group as the data function gives it.
fg_kind() {
  fg_data | awk -F'|' -v g="$1" '$1 == g { print $4; exit }'
}

# undisp: the findings of the review note without a disposition, one per line as "id TAB severity TAB quote".
undisp_skip() {
  awk -F'|' -v p="$FPFX-" -v skip=" $1 " '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { on = ($0 == "## Findings"); next }
    on && index($0, "| " p) == 1 {
      if (trim($6) == "" && index(skip, " " trim($2) " ") == 0) {
        q = trim($4); sub(/^.*quote "/, "", q); sub(/"$/, "", q)
        print trim($2) "\t" trim($3) "\t" q
      }
    }
  ' "$NT"
}
# undisp: in profile 5 the findings that the addendum dispositions are dropped too.
undisp() {
  if [ "$ROUND" -ge 5 ]; then undisp_skip "$(add_ids | tr '\n' ' ')"; else undisp_skip ""; fi
}

# base_ids: the ids of the findings of the review note whose reference names the file BASE (the base text is not
# edited by any plan, so the quoted sentence of such a finding is not looked up in the specification).
base_ids() {
  awk -F'|' -v p="$FPFX-" '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { on = ($0 == "## Findings"); next }
    on && index($0, "| " p) == 1 && index($4, " file BASE;") > 0 { print trim($2) }
  ' "$NT"
}

# od_data: the fixed texts of the three decisions of round 3. One record per line, fields separated by a vertical
# bar: "D|id|header|finding" opens a decision, "Q|question" is its question, "O|label|description" is one option.
# No option is recommended.
od_data() {
  if [ "$ROUND" -eq 7 ]; then
    cat << 'DATA7'
D|OD-12|Soft failure|RH-C-001
Q|The text says that a change which waits for a human decision on a soft failure ends that wait only by the fail action or by an override, and it also lets the cancel and supersede actions close such a change as cancelled. How should a cancel or supersede of such a change end it?
O|Close as failed|A cancel or supersede of such a change closes it as failed, not as cancelled.
O|Allow cancelled|A cancel or supersede of such a change may close it as cancelled, and the text says so where it now says that the wait ends only by fail or override.
D|OD-13|Ignore file|RH-X-002
Q|The scope rule does not measure a path that an ignore file inside the repository hides, and it does not say which version of that file counts, so a change could first edit the ignore file and then work in the paths it now hides. What should the text say?
O|Base revision only|Only the ignore files as they were at the base revision hide paths, so an ignore file that the change creates or alters hides nothing.
O|Forbid editing it|A change may not create or alter an ignore file inside the repository, and doing so is a scope violation even when the allowed path list matches the file.
DATA7
    return 0
  fi
  if [ "$ROUND" -eq 6 ]; then
    cat << 'DATA6'
D|OD-10|Replacement|RG-C-001
Q|The supersede action only requires that the replacement is a different change that exists, and the text does not say whether that change may already be closed. Which replacement should be allowed?
O|Not closed|The replacement must be a change that is not closed; a closed change is refused.
O|Not closed, or done|The replacement must be a change that is not closed, or one that closed as done; one that closed as failed, cancelled or superseded is refused.
D|OD-11|Spec drift|RG-X-001
Q|The text protects the specification file (spec.md) of a core change against later edits only after it was approved once, and a project does not always require that approval. How should this be fixed?
O|Record its hash|The content hash of spec.md is recorded whenever the specification is anchored, so that a later edit is detected even if approval was never required.
O|Always approve it|The approval of spec.md is required for every core change, not only when the compliance profile or the project configuration requires it.
O|Say it openly|The text says plainly that spec.md is protected only after it was approved, and that otherwise only change.yaml is a machine-checkable anchor.
DATA6
    return 0
  fi
  if [ "$ROUND" -eq 5 ]; then
    cat << 'DATA5'
D|OD-6|Templates|RF-X-001
Q|Sections 16.1 to 16.4 apply to the full profile only, and none of their rules has an acceptance example. How should this be fixed?
O|Add examples|Examples are added that show these rules, in the same layout as the existing examples.
O|Say none needed|The text says plainly that these rules need no example of their own, and gives the reason that you state.
D|OD-7|ADR rules|RF-X-002
Q|The rules of Section 13 (conflict with an ADR, specification drift, breaking changes) have no acceptance example. How should this be fixed?
O|Add examples|Examples are added that show these rules, in the same layout as the existing examples.
O|Say none needed|The text says plainly that these rules need no example of their own, and gives the reason that you state.
D|OD-8|Review rules|RF-X-003
Q|The rules of Sections 14.3 to 14.5 (the review cycle, findings and review artifacts) have no acceptance example. How should this be fixed?
O|Add examples|Examples are added that show these rules, in the same layout as the existing examples.
O|Say none needed|The text says plainly that these rules need no example of their own, and gives the reason that you state.
D|OD-9|Agent bans|RF-X-004
Q|The prohibitions on an AI agent in Section 19.1 have no acceptance example. How should this be fixed?
O|Add examples|Examples are added that show these rules, in the same layout as the existing examples.
O|Say none needed|The text says plainly that these rules need no example of their own, and gives the reason that you state.
DATA5
    return 0
  fi
  if [ "$ROUND" -eq 4 ]; then
    cat << 'DATA4'
D|OD-4|Supersede|RT-A-001
Q|After the gate definitions of a change were edited, may the `supersede` action still go ahead?
O|Cancel only|Only `cancel` still goes ahead, and `supersede` is refused until a human approves the edited checks again.
O|Supersede too, said openly|`supersede` still goes ahead beside `cancel`, and the text says so plainly and says why.
D|OD-5|Retry limit|RT-B-001
Q|Should reaching a retry limit end the change by itself, or pause it for a human?
O|Soft, said openly|A retry limit stays a pause for a human, and the text says plainly that the earlier text ended the flow there.
O|Hard or soft|A retry limit can be set to end the change by itself or to pause it for a human, like any other failure condition.
O|Hard only|Reaching a retry limit always ends the change by itself, as in the earlier text, and a retry limit cannot be set to pause.
DATA4
    return 0
  fi
  cat << 'DATA'
D|OD-1|Guard anchor|RR-B-001
Q|What should `guard` do for a change whose history uses an equivalent mechanism instead of an anchor?
O|Accept an equivalent|`guard` passes the history check when the history has an anchor or an equivalent mechanism, in the words of the history rules.
O|Anchor only, said openly|`guard` checks for an anchor only and the text says so; a change that uses an equivalent mechanism is reported as missing its anchor.
D|OD-2|Ignore settings|RR-X-001
Q|How should the scope check treat the settings that tell version control to ignore files?
O|Repository files only|only ignore files inside the repository count; they are ordinary files, so changing one is a changed path that needs an allowed path, and ignore settings kept elsewhere are not applied.
O|Detect any change|the ignore settings from every place version control reads are recorded when the change starts, and any later difference is a scope violation.
O|Measure every file|every file counts, ignored or not; a project that wants a build folder left out lists it in the allowed paths.
O|Say it openly|the check stays as it is and the text says plainly that ignore settings, wherever kept, are trusted, so work they hide is not measured.
D|OD-3|Fail action|RR-X-002
Q|When should the `fail` action be allowed in the full profile?
O|Soft failures only|`fail` is allowed only while a soft failure waits for a human, as the section on hard and soft failure says; with only a hard failure active it is refused.
O|Any active failure|`fail` is allowed whenever a failure condition is active, hard or soft; it ends the change as failed and answers success, and the section on hard and soft failure is reworded to say so.
DATA
}

# od_summary ID: the Summary cell of the finding in the findings table of the review note, verbatim.
od_summary() {
  awk -F'|' -v id="$1" '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { on = ($0 == "## Findings"); next }
    on && trim($2) == id { print trim($5); exit }
  ' "$NT"
}

# od_sev ID: the severity of the finding in the findings table of the review note.
od_sev() {
  awk -F'|' -v id="$1" '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { on = ($0 == "## Findings"); next }
    on && trim($2) == id { print trim($3); exit }
  ' "$NT"
}

# print_od_questions: the three decisions as the owner is asked them.
print_od_questions() {
  local tag a b c first=1 sum sev
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D)
        if [ "$first" -eq 0 ]; then printf '\n'; fi
        first=0
        sum=$(od_summary "$c")
        sev=$(od_sev "$c")
        if [ -z "$sum" ] || [ -z "$sev" ]; then echo "cannot read the finding $c from the review note" >&2; exit 2; fi
        printf '%s %s\nFinding: %s (%s)\nThe reviewer says: %s\n' "$a" "$b" "$c" "$sev" "$sum" ;;
      Q) printf 'Question: %s\n' "$a" ;;
      O) printf -- '- %s: %s\n' "$a" "$b" ;;
    esac
  done < <(od_data)
}

# od_labels ID: the option labels of one decision, one per line.
od_labels() {
  local tag a b c cur=""
  while IFS='|' read -r tag a b c; do
    case "$tag" in
      D) cur=$a ;;
      O) if [ "$cur" = "$1" ]; then printf '%s\n' "$a"; fi ;;
    esac
  done < <(od_data)
}

# print_register_skeleton: the fix register with every field that is filled in later set to pending.
print_register_skeleton() {
  local g t f k id sev b h1="$REG_H1" intro="$REG_INTRO"
  if [ "$ROUND" -eq 3 ]; then h1="$REG3_H1"; intro="$REG3_INTRO"; fi
  if [ "$ROUND" -eq 4 ]; then h1="$REG4_H1"; intro="$REG4_INTRO"; fi
  if [ "$ROUND" -eq 5 ]; then h1="$REG5_H1"; intro="$REG5_INTRO"; fi
  if [ "$ROUND" -eq 6 ]; then h1="$REG6_H1"; intro="$REG6_INTRO"; fi
  if [ "$ROUND" -eq 7 ]; then h1="$REG7_H1"; intro="$REG7_INTRO"; fi
  printf '%s\n\n%s\n\n' "$h1" "$intro"
  printf '%s\n\n| Change | Title | Findings | Kind | Status | Sections | Examples |\n|---|---|---|---|---|---|---|\n' "$REG_TBL_H"
  while IFS='|' read -r g t f k; do
    printf '| %s | %s | %s | %s | pending | - | - |\n' "$g" "$t" "$f" "$k"
  done < <(fg_data)
  printf '\n## Change details\n\n'
  while IFS='|' read -r g t f k; do
    printf '### %s — %s\n\n' "$g" "$t"
    for b in "${REG_BULLETS[@]}"; do printf -- '- %s: pending\n' "$b"; done
    printf '\n'
  done < <(fg_data)
  printf '## Normative lines removed or reworded\n\nNone.\n\n## Findings whose quoted sentence an edit touched\n\nNone.\n\n## Findings not touched\n\n'
  while IFS=$'\t' read -r id sev _; do
    printf -- '- %s (%s): open information; no edit\n' "$id" "$sev"
  done < <(undisp)
  printf '\n## Header\n\n%s\n' "$REG_HEADER"
}

# ---- the disposition addendum (profile 5: of round 4, profile 6: of round 5) -------------------------------------

# AD is the working copy of the addendum (an empty file when it does not exist), AD_OK says whether it was read.
AD="$TMP/addendum"
AD_OK=0
if [ "$ROUND" -ge 5 ]; then
  if [ "$ADD_RND" -gt 0 ] && [ -f "$ADDENDUM" ] && [ -r "$ADDENDUM" ] && cp "$ADDENDUM" "$AD" 2> /dev/null; then AD_OK=1; else : > "$AD"; fi
  NCHG=$(fg_data | wc -l | tr -d ' ')
  case "$NCHG" in
    0) NCHG_W="zero" ;;
    1) NCHG_W="one" ;;
    2) NCHG_W="two" ;;
    3) NCHG_W="three" ;;
    4) NCHG_W="four" ;;
    5) NCHG_W="five" ;;
    6) NCHG_W="six" ;;
    *) NCHG_W="seven" ;;
  esac
  NUNDISP=$((NUNDISP_BASE - $(add_ids | wc -l | tr -d ' ')))
fi

AD_NAME_Q='Under which name or handle should these dispositions be recorded for the repository owner?'
AD_DATE_Q='Which date are these dispositions given? Give it as YYYY-MM-DD.'
AD_COPIED=("Reviewed file" "Base blob" "Result blob" "Reviewed SHA-256" "Line count" "Diffstat" "Commits touching the file")
AD_LABELS=("${AD_COPIED[@]}" "Review note file" "Reports SHA-256" "Disposition record file" "Disposition record blob" "Dispositions given by" "Owner reply" "Check results")

# reports_sha: the SHA-256 of the Reports section of the review note, computed as the review check script computes it.
reports_sha() {
  awk -v sect="Reports" '/^```/ { fence = !fence } !fence && /^## / { on = ($0 == "## " sect); next } on' "$NT" | sha256sum | cut -d ' ' -f1
}

# disp_q ID: the Question line that the review check script prints for the finding ID.
disp_q() {
  bash "$CHK" --round "$ADD_RND" --print-disposition-skeleton --finding "$1" 2> /dev/null | grep -m1 '^- Question: '
}

# print_addendum_skeleton: the addendum in its unfilled form (the only way it is created).
print_addendum_skeleton() {
  local id l x drb list dup sel
  list=${ADS_FINDINGS:-$AD_DEFAULT_IDS}
  list=${list// /}
  sel=""
  for x in ${list//,/ }; do
    if ! [[ "$x" =~ ^$FPFX-[A-Z]-[0-9]{3}$ ]]; then echo "--findings: [$x] is not a finding id" >&2; exit 2; fi
    case " $sel " in *" $x "*) echo "--findings: $x occurs twice" >&2; exit 2 ;; esac
    sel="$sel $x"
  done
  if [ -z "$sel" ]; then echo "--findings names no finding" >&2; exit 2; fi
  undisp_skip "" | cut -f1 > "$TMP/ads.avail"
  awk '/^### / { print $2 }' "$DR" > "$TMP/ads.drids"
  for x in $sel; do
    if grep -q -x -F -e "$x" "$TMP/ads.drids"; then echo "--findings: $x is dispositioned by the disposition record" >&2; exit 2; fi
    if ! grep -q -x -F -e "$x" "$TMP/ads.avail"; then echo "--findings: $x is no finding of the review note without a disposition" >&2; exit 2; fi
  done
  drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || { echo "cannot read the disposition record at HEAD" >&2; exit 2; }
  parse_pins "$DR" "$TMP/dr.pins"
  for l in "${AD_COPIED[@]}" "Reports SHA-256"; do
    if [ -z "$(pin_raw "$TMP/dr.pins" "$l")" ]; then echo "the disposition record has no row [$l]" >&2; exit 2; fi
  done
  : > "$TMP/ads.blocks"
  while IFS= read -r id; do
    case " $sel " in *" $id "*) ;; *) continue ;; esac
    bash "$CHK" --round "$ADD_RND" --print-disposition-skeleton --finding "$id" >> "$TMP/ads.blocks" 2> /dev/null || { echo "cannot print the block of $id" >&2; exit 2; }
  done < "$TMP/ads.avail"
  dup=$(grep -c '^### ' "$TMP/ads.blocks")
  if [ "$dup" -eq 0 ]; then echo "no block could be printed" >&2; exit 2; fi
  printf '%s\n\n' "$AD_H1"
  printf -- '- Owner disposition date: %s\n\n' "$FILL"
  printf '| Field | Value |\n|---|---|\n'
  for l in "${AD_COPIED[@]}"; do printf '| %s | %s |\n' "$l" "$(pin_raw "$TMP/dr.pins" "$l")"; done
  printf '| Review note file | `%s` |\n' "$NOTE_DEFAULT"
  printf '| Reports SHA-256 | %s |\n' "$(pin_raw "$TMP/dr.pins" "Reports SHA-256")"
  printf '| Disposition record file | `%s` |\n' "$DREC_DEFAULT"
  printf '| Disposition record blob | `%s` |\n' "$drb"
  printf '| Dispositions given by | %s |\n| Owner reply | %s |\n| Check results | %s |\n\n' "$FILL" "$FILL" "$FILL"
  printf '## Findings dispositioned by the owner\n\n'
  cat "$TMP/ads.blocks"
  printf '## Reply details\n\n### Name\n\n- Question: %s\n- Answer: %s\n\n### Date\n\n- Question: %s\n- Answer: %s\n\n' "$AD_NAME_Q" "$FILL" "$AD_DATE_Q" "$FILL"
  printf '## What follows\n\n%s\n\n%s\n' "$AD_FOLLOWS_TEXT" "$CLOSING_LINE"
}

if [ "$PRINT_ADS" -eq 1 ]; then
  print_addendum_skeleton
  exit 0
fi

if [ "$PRINT_Q" -eq 1 ]; then
  print_od_questions
  exit 0
fi

if [ "$PRINT_REG" -eq 1 ]; then
  print_register_skeleton
  exit 0
fi

if [ "$PRINT_SKEL" -eq 1 ]; then
  print_skeleton
  exit 0
fi

# ST1 and ST2: the pins of round 1 and the state of the specification.
state_stage() {
  local m="" n_out n_ok t
  n_out=$(grep -c '^- Owner approval: ' "$AR")
  n_ok=$(grep -c '^- Owner approval: approved$' "$AR")
  if [ "$n_out" -ne 1 ] || [ "$n_ok" -ne 1 ]; then
    m="the approval record does not hold exactly one outcome line [- Owner approval: approved]"
  fi
  for t in "Result blob" "Reviewed SHA-256" "Line count"; do
    if [ -n "$m" ]; then break; fi
    if [ "$(pin_count "$TMP/arc.pins" "$t")" -ne 1 ]; then m="the approval record does not hold the pin row [$t] exactly once"; fi
    if [ "$(pin_count "$TMP/dr.pins" "$t")" -ne 1 ]; then m="the disposition record does not hold the pin row [$t] exactly once"; fi
  done
  if [ -z "$m" ]; then
    if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then m="the result blob of the approval record is not 40 lowercase hexadecimal digits"
    elif ! [[ "$A_SHA" =~ ^[0-9a-f]{64}$ ]]; then m="the SHA-256 of the approval record is not 64 lowercase hexadecimal digits"
    elif ! [[ "$A_LINES" =~ ^[0-9]+$ ]]; then m="the line count of the approval record is not an integer"
    elif [ "$A_BLOB" != "$D_BLOB" ]; then m="the result blob of the disposition record differs from the approval record"
    elif [ "$A_SHA" != "$D_SHA" ]; then m="the SHA-256 of the disposition record differs from the approval record"
    elif [ "$A_LINES" != "$D_LINES" ]; then m="the line count of the disposition record differs from the approval record"
    fi
  fi
  if [ -n "$m" ]; then
    fail ST1 "$m"
    return 0
  fi
  pass ST1 "the approved round-1 text is pinned identically by the approval record and the disposition record (blob, SHA-256, $A_LINES lines)"
  local w i h
  w=$(git hash-object -- "$SPECFILE" 2> /dev/null) || w=""
  i=$(git rev-parse --verify --quiet ":$SPEC" 2> /dev/null) || i=""
  h=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || h=""
  if [ "$w" = "$A_BLOB" ] && [ "$i" = "$A_BLOB" ] && [ "$h" = "$A_BLOB" ]; then
    echo "STATE: the specification equals the text of round 1 (all round-1 live checks apply)"
  else
    echo "STATE: the specification differs from the text of round 1 (the live checks that pin the round-1 text fail by design; use --replay-round-1)"
  fi
}

# find_round1_commit BLOB: print the newest commit reachable from HEAD at which the specification holds BLOB.
find_round1_commit() {
  git rev-list HEAD > "$TMP/revs" 2> /dev/null || return 1
  sed "s|\$|:$SPEC|" "$TMP/revs" | git cat-file --batch-check='%(objectname)' > "$TMP/objs" 2> /dev/null
  paste -d' ' "$TMP/revs" "$TMP/objs" | awk -v b="$1" '$2 == b { print $1; exit }'
}

# run_in_clone LABEL SCRIPT [ARGS]: run a script of the clone inside the clone; print its last line in $LAST and
# return 0 when it ended with RESULT: PASS and exit status 0.
run_in_clone() {
  local script=$1 rc
  shift
  (cd "$CL" && bash "$script" "$@") > "$TMP/run.out" 2>&1
  rc=$?
  LAST=$(tail -n1 "$TMP/run.out")
  [ "$rc" -eq 0 ] && [ "$LAST" = "RESULT: PASS" ]
}

# replay: FR1 to FR5.
replay() {
  local c om cm t
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail FR1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail FR1 "no commit reachable from HEAD holds the specification with the round-1 blob"
    return 0
  fi
  if ! git cat-file -e "$c:$ARC_DEFAULT" 2> /dev/null || ! git cat-file -e "$c:$DREC_DEFAULT" 2> /dev/null; then
    fail FR1 "the commit that holds the round-1 text does not hold both round-1 records: the round-1 evidence is not in the history"
    return 0
  fi
  pass FR1 "found the newest commit reachable from HEAD that holds the round-1 text and both round-1 records"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail FR1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail FR1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass FR2 "the drafting check with --final at the round-1 commit: $LAST"; else fail FR2 "the drafting check with --final at the round-1 commit: $LAST"; fi
  if run_in_clone "$CHK3" --stage recorded; then pass FR3 "the owner approval check in stage recorded at the round-1 commit: $LAST"; else fail FR3 "the owner approval check in stage recorded at the round-1 commit: $LAST"; fi
  if run_in_clone "$CHK" --stage dispositioned; then pass FR4 "the review check in stage dispositioned at the round-1 commit: $LAST"; else fail FR4 "the review check in stage dispositioned at the round-1 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK3" "$CHK"; do
      if ! cp "$t" "$CL/$t" 2> /dev/null; then fail FR5 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    local r2 r3 r4=""
    r2=PASS; r3=PASS; r4=PASS
    run_in_clone "$CHK2" --final || r2="FAIL ($LAST)"
    run_in_clone "$CHK3" --stage recorded || r3="FAIL ($LAST)"
    run_in_clone "$CHK" --stage dispositioned || r4="FAIL ($LAST)"
    if [ "$r2" = PASS ] && [ "$r3" = PASS ] && [ "$r4" = PASS ]; then
      pass FR5 "the current versions of the three scripts also end RESULT: PASS at the round-1 commit"
    else
      fail FR5 "the current versions of the three scripts at the round-1 commit: drafting check $r2, owner approval check $r3, review check $r4"
    fi
  fi
}

# replay2: R2-1 to R2-8, the checks of the fix round of round 2 at the commit that holds the text of round 2.
replay2() {
  local c om cm t f st
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail R2-1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail R2-1 "no commit reachable from HEAD holds the specification with the round-2 blob"
    return 0
  fi
  for f in "$ARC2_PATH" "$DREC2_PATH" "$NOTE2_PATH" "$FREG2_PATH" "$APK2_PATH" "$BRIEF2_PATH"; do
    if ! git cat-file -e "$c:$f" 2> /dev/null; then
      fail R2-1 "the commit that holds the round-2 text does not hold all six round-2 files: the round-2 evidence is not in the history"
      return 0
    fi
  done
  pass R2-1 "found the newest commit reachable from HEAD that holds the round-2 text and the six round-2 files"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail R2-1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail R2-1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass R2-2 "the drafting check with --final at the round-2 commit: $LAST"; else fail R2-2 "the drafting check with --final at the round-2 commit: $LAST"; fi
  if run_in_clone "$FIXP" --stage edits --complete; then pass R2-3 "the fix round check in stage edits with --complete at the round-2 commit: $LAST"; else fail R2-3 "the fix round check in stage edits with --complete at the round-2 commit: $LAST"; fi
  if run_in_clone "$FIXP" --stage approval-pending; then pass R2-4 "the fix round check in stage approval-pending at the round-2 commit: $LAST"; else fail R2-4 "the fix round check in stage approval-pending at the round-2 commit: $LAST"; fi
  if run_in_clone "$FIXP" --stage approval-recorded; then pass R2-5 "the fix round check in stage approval-recorded at the round-2 commit: $LAST"; else fail R2-5 "the fix round check in stage approval-recorded at the round-2 commit: $LAST"; fi
  if replay2_brief; then pass R2-6 "the review check with --round 2 prints the review brief of round 2 character for character at the round-2 commit"; else fail R2-6 "the review check with --round 2 does not print the review brief of round 2 at the round-2 commit"; fi
  if run_in_clone "$CHK" --round 2 --stage dispositioned; then pass R2-7 "the review check with --round 2 in stage dispositioned at the round-2 commit: $LAST"; else fail R2-7 "the review check with --round 2 in stage dispositioned at the round-2 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK" "$FIXP"; do
      if ! cp "$ROOT/$t" "$CL/$t" 2> /dev/null; then fail R2-8 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    st=""
    run_in_clone "$CHK2" --final || st="$st drafting check ($LAST);"
    run_in_clone "$FIXP" --stage edits --complete || st="$st edits ($LAST);"
    run_in_clone "$FIXP" --stage approval-pending || st="$st approval-pending ($LAST);"
    run_in_clone "$FIXP" --stage approval-recorded || st="$st approval-recorded ($LAST);"
    replay2_brief || st="$st review brief;"
    run_in_clone "$CHK" --round 2 --stage dispositioned || st="$st dispositioned ($LAST);"
    if [ -z "$st" ]; then
      pass R2-8 "the current versions of the three scripts also pass the six runs at the round-2 commit"
    else
      fail R2-8 "the current versions of the three scripts at the round-2 commit fail:$st"
    fi
  fi
}

# replay3: R3-1 to R3-8, the checks of the fix round of round 3 at the commit that holds the text of round 3.
replay3() {
  local c om cm t f st
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail R3-1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail R3-1 "no commit reachable from HEAD holds the specification with the round-3 blob"
    return 0
  fi
  for f in "$ARC3_PATH" "$DREC3_PATH" "$NOTE3_PATH" "$FREG3_PATH" "$APK3_PATH" "$BRIEF3_PATH"; do
    if ! git cat-file -e "$c:$f" 2> /dev/null; then
      fail R3-1 "the commit that holds the round-3 text does not hold all six round-3 files: the round-3 evidence is not in the history"
      return 0
    fi
  done
  pass R3-1 "found the newest commit reachable from HEAD that holds the round-3 text and the six round-3 files"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail R3-1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail R3-1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass R3-2 "the drafting check with --final at the round-3 commit: $LAST"; else fail R3-2 "the drafting check with --final at the round-3 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 3 --stage edits --complete; then pass R3-3 "the fix round check with --round 3 in stage edits with --complete at the round-3 commit: $LAST"; else fail R3-3 "the fix round check with --round 3 in stage edits with --complete at the round-3 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 3 --stage approval-pending; then pass R3-4 "the fix round check with --round 3 in stage approval-pending at the round-3 commit: $LAST"; else fail R3-4 "the fix round check with --round 3 in stage approval-pending at the round-3 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 3 --stage approval-recorded; then pass R3-5 "the fix round check with --round 3 in stage approval-recorded at the round-3 commit: $LAST"; else fail R3-5 "the fix round check with --round 3 in stage approval-recorded at the round-3 commit: $LAST"; fi
  if replay3_brief; then pass R3-6 "the review check with --round 3 prints the review brief of round 3 character for character at the round-3 commit"; else fail R3-6 "the review check with --round 3 does not print the review brief of round 3 at the round-3 commit"; fi
  if run_in_clone "$CHK" --round 3 --stage dispositioned; then pass R3-7 "the review check with --round 3 in stage dispositioned at the round-3 commit: $LAST"; else fail R3-7 "the review check with --round 3 in stage dispositioned at the round-3 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK" "$FIXP"; do
      if ! cp "$ROOT/$t" "$CL/$t" 2> /dev/null; then fail R3-8 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    st=""
    run_in_clone "$CHK2" --final || st="$st drafting check ($LAST);"
    run_in_clone "$FIXP" --round 3 --stage edits --complete || st="$st edits ($LAST);"
    run_in_clone "$FIXP" --round 3 --stage approval-pending || st="$st approval-pending ($LAST);"
    run_in_clone "$FIXP" --round 3 --stage approval-recorded || st="$st approval-recorded ($LAST);"
    replay3_brief || st="$st review brief;"
    run_in_clone "$CHK" --round 3 --stage dispositioned || st="$st dispositioned ($LAST);"
    if [ -z "$st" ]; then
      pass R3-8 "the current versions of the three scripts also pass the six runs at the round-3 commit"
    else
      fail R3-8 "the current versions of the three scripts at the round-3 commit fail:$st"
    fi
  fi
}

# replay3_brief: in the clone, the review check with --round 3 prints the review brief of round 3 character for
# character.
replay3_brief() {
  (cd "$CL" && bash "$CHK" --round 3 --print-brief) > "$TMP/brief.out" 2> /dev/null || return 1
  cmp -s "$TMP/brief.out" "$CL/$BRIEF3_PATH"
}

# replay4: R4-1 to R4-8, the checks of the fix round of round 4 at the commit that holds the text of round 4.
replay4() {
  local c om cm t f st
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail R4-1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail R4-1 "no commit reachable from HEAD holds the specification with the round-4 blob"
    return 0
  fi
  for f in "$ARC4_PATH" "$DREC4_PATH" "$NOTE4_PATH" "$FREG4_PATH" "$APK4_PATH" "$BRIEF4_PATH"; do
    if ! git cat-file -e "$c:$f" 2> /dev/null; then
      fail R4-1 "the commit that holds the round-4 text does not hold all six round-4 files: the round-4 evidence is not in the history"
      return 0
    fi
  done
  pass R4-1 "found the newest commit reachable from HEAD that holds the round-4 text and the six round-4 files"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail R4-1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail R4-1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass R4-2 "the drafting check with --final at the round-4 commit: $LAST"; else fail R4-2 "the drafting check with --final at the round-4 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 4 --stage edits --complete; then pass R4-3 "the fix round check with --round 4 in stage edits with --complete at the round-4 commit: $LAST"; else fail R4-3 "the fix round check with --round 4 in stage edits with --complete at the round-4 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 4 --stage approval-pending; then pass R4-4 "the fix round check with --round 4 in stage approval-pending at the round-4 commit: $LAST"; else fail R4-4 "the fix round check with --round 4 in stage approval-pending at the round-4 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 4 --stage approval-recorded; then pass R4-5 "the fix round check with --round 4 in stage approval-recorded at the round-4 commit: $LAST"; else fail R4-5 "the fix round check with --round 4 in stage approval-recorded at the round-4 commit: $LAST"; fi
  if replay4_brief; then pass R4-6 "the review check with --round 4 prints the review brief of round 4 character for character at the round-4 commit"; else fail R4-6 "the review check with --round 4 does not print the review brief of round 4 at the round-4 commit"; fi
  if run_in_clone "$CHK" --round 4 --stage dispositioned; then pass R4-7 "the review check with --round 4 in stage dispositioned at the round-4 commit: $LAST"; else fail R4-7 "the review check with --round 4 in stage dispositioned at the round-4 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK" "$FIXP"; do
      if ! cp "$ROOT/$t" "$CL/$t" 2> /dev/null; then fail R4-8 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    st=""
    run_in_clone "$CHK2" --final || st="$st drafting check ($LAST);"
    run_in_clone "$FIXP" --round 4 --stage edits --complete || st="$st edits ($LAST);"
    run_in_clone "$FIXP" --round 4 --stage approval-pending || st="$st approval-pending ($LAST);"
    run_in_clone "$FIXP" --round 4 --stage approval-recorded || st="$st approval-recorded ($LAST);"
    replay4_brief || st="$st review brief;"
    run_in_clone "$CHK" --round 4 --stage dispositioned || st="$st dispositioned ($LAST);"
    if [ -z "$st" ]; then
      pass R4-8 "the current versions of the three scripts also pass the six runs at the round-4 commit"
    else
      fail R4-8 "the current versions of the three scripts at the round-4 commit fail:$st"
    fi
  fi
}

# replay4_brief: in the clone, the review check with --round 4 prints the review brief of round 4 character for
# character.
replay4_brief() {
  (cd "$CL" && bash "$CHK" --round 4 --print-brief) > "$TMP/brief.out" 2> /dev/null || return 1
  cmp -s "$TMP/brief.out" "$CL/$BRIEF4_PATH"
}

# replay5: R5-1 to R5-8, the checks of the fix round of round 5 at the commit that holds the text of round 5.
replay5() {
  local c om cm t f st
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then
    fail R5-1 "the result blob of the approval record is not 40 lowercase hexadecimal digits"
    return 0
  fi
  c=$(find_round1_commit "$A_BLOB")
  if [ -z "$c" ]; then
    fail R5-1 "no commit reachable from HEAD holds the specification with the round-5 blob"
    return 0
  fi
  for f in "$ARC5_PATH" "$DREC5_PATH" "$NOTE5_PATH" "$FREG5_PATH" "$APK5_PATH" "$BRIEF5_PATH" "$DADD4_PATH"; do
    if ! git cat-file -e "$c:$f" 2> /dev/null; then
      fail R5-1 "the commit that holds the round-5 text does not hold all seven round-5 files: the round-5 evidence is not in the history"
      return 0
    fi
  done
  pass R5-1 "found the newest commit reachable from HEAD that holds the round-5 text and the seven round-5 files"
  CL="$TMP/clone"
  if ! git clone --local --no-checkout --quiet -- "$ROOT" "$CL" > /dev/null 2>&1; then
    fail R5-1 "the throwaway clone could not be made"
    return 0
  fi
  if ! git -C "$CL" checkout --quiet --detach "$c" > /dev/null 2>&1; then
    fail R5-1 "the commit could not be checked out in the throwaway clone"
    return 0
  fi
  om=$(git rev-parse --verify --quiet "$BASE^{commit}")
  cm=$(git -C "$CL" rev-parse --verify --quiet "origin/main^{commit}" 2> /dev/null) || cm=""
  if [ "$cm" != "$om" ]; then
    git -C "$CL" update-ref refs/remotes/origin/main "$om" > /dev/null 2>&1
  fi
  if run_in_clone "$CHK2" --final; then pass R5-2 "the drafting check with --final at the round-5 commit: $LAST"; else fail R5-2 "the drafting check with --final at the round-5 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 5 --stage edits --complete; then pass R5-3 "the fix round check with --round 5 in stage edits with --complete at the round-5 commit: $LAST"; else fail R5-3 "the fix round check with --round 5 in stage edits with --complete at the round-5 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 5 --stage approval-pending; then pass R5-4 "the fix round check with --round 5 in stage approval-pending at the round-5 commit: $LAST"; else fail R5-4 "the fix round check with --round 5 in stage approval-pending at the round-5 commit: $LAST"; fi
  if run_in_clone "$FIXP" --round 5 --stage approval-recorded; then pass R5-5 "the fix round check with --round 5 in stage approval-recorded at the round-5 commit: $LAST"; else fail R5-5 "the fix round check with --round 5 in stage approval-recorded at the round-5 commit: $LAST"; fi
  if replay5_brief; then pass R5-6 "the review check with --round 5 prints the review brief of round 5 character for character at the round-5 commit"; else fail R5-6 "the review check with --round 5 does not print the review brief of round 5 at the round-5 commit"; fi
  if run_in_clone "$CHK" --round 5 --stage dispositioned; then pass R5-7 "the review check with --round 5 in stage dispositioned at the round-5 commit: $LAST"; else fail R5-7 "the review check with --round 5 in stage dispositioned at the round-5 commit: $LAST"; fi
  if [ "$CURRENT" -eq 1 ]; then
    for t in "$CHK2" "$CHK" "$FIXP"; do
      if ! cp "$ROOT/$t" "$CL/$t" 2> /dev/null; then fail R5-8 "the current version of a script could not be copied into the clone"; return 0; fi
    done
    st=""
    run_in_clone "$CHK2" --final || st="$st drafting check ($LAST);"
    run_in_clone "$FIXP" --round 5 --stage edits --complete || st="$st edits ($LAST);"
    run_in_clone "$FIXP" --round 5 --stage approval-pending || st="$st approval-pending ($LAST);"
    run_in_clone "$FIXP" --round 5 --stage approval-recorded || st="$st approval-recorded ($LAST);"
    replay5_brief || st="$st review brief;"
    run_in_clone "$CHK" --round 5 --stage dispositioned || st="$st dispositioned ($LAST);"
    if [ -z "$st" ]; then
      pass R5-8 "the current versions of the three scripts also pass the six runs at the round-5 commit"
    else
      fail R5-8 "the current versions of the three scripts at the round-5 commit fail:$st"
    fi
  fi
}

# replay5_brief: in the clone, the review check with --round 5 prints the review brief of round 5 character for
# character.
replay5_brief() {
  (cd "$CL" && bash "$CHK" --round 5 --print-brief) > "$TMP/brief.out" 2> /dev/null || return 1
  cmp -s "$TMP/brief.out" "$CL/$BRIEF5_PATH"
}

# replay2_brief: in the clone, the review check with --round 2 prints the review brief of round 2 character for
# character (the stage brief of the review check is meaningful before the reports are captured only).
replay2_brief() {
  (cd "$CL" && bash "$CHK" --round 2 --print-brief) > "$TMP/brief.out" 2> /dev/null || return 1
  cmp -s "$TMP/brief.out" "$CL/$BRIEF2_PATH"
}

# ---- stage decisions -------------------------------------------------------------------------------------

# h2sec FILE NAME: the lines under the H2 heading NAME. h3blk FILE HEADING: the lines under the H3 line HEADING.
h2sec() { awk -v s="$2" '/^## / { on = ($0 == "## " s); next } on' "$1"; }
h3blk() { awk -v h="$2" '/^#+ / { on = ($0 == h); next } on' "$1"; }

# line_val PREFIX FILE: the value of the first line of FILE that begins with PREFIX (the text after the prefix,
# one leading space removed).
line_val() {
  awk -v p="$1" 'index($0, p) == 1 { v = substr($0, length(p) + 1); sub(/^ /, "", v); print v; exit }' "$2"
}

trim_ws() { printf '%s' "$1" | sed 's/^[ ]*//; s/[ ]*$//'; }

decisions_stage() {
  local id hd m lbl ok cnt val exp_q rec_q

  print_skeleton > "$TMP/exp"

  # FD1
  m=$(enc1 "$DC")
  if [ -z "$m" ]; then m=$(enc2 "$DC"); fi
  if [ -z "$m" ] && grep -v '^#' "$DC" | grep -q -F "$FILL"; then
    m="a fill marker is left in a field (line $(grep -n -F "$FILL" "$DC" | head -n1 | cut -d: -f1))"
  fi
  if [ -z "$m" ]; then
    m=$(fd1_scan "$DC")
  fi
  if [ -n "$m" ]; then fail FD1 "$m"; else pass FD1 "encoding, line endings, fill markers and self-containment are in order"; fi

  # FD2
  m=""
  if [ "$(head -n1 "$DC")" != "$H1_LINE" ]; then
    m="the first line is not the H1 [$H1_LINE]"
  elif [ "$(grep -c '^- Decisions given by:' "$DC")" -ne 1 ] || [ "$(grep -c '^- Owner decision date:' "$DC")" -ne 1 ]; then
    m="the lines [- Decisions given by:] and [- Owner decision date:] do not occur exactly once each"
  elif ! cmp -s <(grep '^## ' "$DC") <(grep '^## ' "$TMP/exp"); then
    m="the H2 headings are not the four expected ones in order"
  elif ! cmp -s <(grep '^### ' "$DC") <(grep '^### ' "$TMP/exp"); then
    m="the H3 headings are not D-1 to D-5, Name and Date, once each in order"
  elif [ "$(tail -n1 "$DC")" != "$CLOSING_LINE" ] || [ "$(grep -c -x -F "$CLOSING_LINE" "$DC")" -ne 1 ]; then
    m="the closing line is not the last line, once"
  fi
  if [ -n "$m" ]; then fail FD2 "$m"; else pass FD2 "H1, header lines, four H2 headings, seven H3 headings and the closing line are in order"; fi

  # FD3
  h2sec "$DC" "The text before the fix round" > "$TMP/t.rec"
  h2sec "$TMP/exp" "The text before the fix round" > "$TMP/t.exp"
  if cmp -s "$TMP/t.rec" "$TMP/t.exp"; then
    pass FD3 "the table of the text before the fix round equals the two round-1 records and the disposition record blob at HEAD"
  else
    m=$(diff "$TMP/t.exp" "$TMP/t.rec" | grep '^[<>] |' | head -n1 | cut -c1-60)
    fail FD3 "the table of the text before the fix round differs from the round-1 records (first difference: ${m:-no row})"
  fi

  # FD4, FD5, FD8 per decision
  local bad4="" bad5="" bad8="" fixids
  fixids=$(drec_fix_ids)
  for id in "${DEC_IDS[@]}"; do
    hd="### $id — $(dec_header "$id")"
    h3blk "$DC" "$hd" > "$TMP/b.rec"
    h3blk "$TMP/exp" "$hd" > "$TMP/b.exp"
    exp_q=$(awk '/^- Question: / || /^- Options:$/ || /^  - /' "$TMP/b.exp")
    rec_q=$(awk '/^- Question: / || /^- Options:$/ || /^  - /' "$TMP/b.rec")
    if [ "$exp_q" != "$rec_q" ]; then bad4="$bad4 $id"; fi

    # FD5
    cnt=$(grep -c '^- Answer:' "$TMP/b.rec")
    if [ "$cnt" -ne 1 ]; then
      bad5="$bad5 $id(answer line count $cnt)"
    else
      val=$(line_val "- Answer:" "$TMP/b.rec")
      ok=0
      while IFS= read -r lbl; do
        if [ "$val" = "$lbl" ]; then ok=1; fi
      done < <(dec_labels "$id")
      if [ "$ok" -eq 0 ]; then bad5="$bad5 $id(answer is not an option label)"; fi
    fi
    cnt=$(grep -c '^- Owner reason:' "$TMP/b.rec")
    if [ "$cnt" -ne 1 ]; then
      bad5="$bad5 $id(reason line count $cnt)"
    else
      val=$(line_val "- Owner reason:" "$TMP/b.rec")
      if [ -z "$(trim_ws "$val")" ] || [ "$val" != "$(trim_ws "$val")" ]; then bad5="$bad5 $id(owner reason empty or padded)"; fi
    fi

    # FD8
    val=$(line_val "- Findings:" "$TMP/b.rec")
    cnt=0
    for f in $(printf '%s\n' "$val" | grep -o -E 'RV-[A-Z]-[0-9]{3}'); do
      cnt=$((cnt + 1))
      if ! printf '%s\n' "$fixids" | grep -q -x -F "$f"; then bad8="$bad8 $id($f is not a finding with the disposition fix)"; fi
    done
    if [ "$cnt" -eq 0 ]; then
      bad8="$bad8 $id(names no finding)"
    elif [ "$val" != "$(dec_findings "$id")" ]; then
      bad8="$bad8 $id(findings line differs from the printed one)"
    fi
  done
  if [ -n "$bad4" ]; then fail FD4 "the Question or Options bullets differ from the printed ones in:$bad4"; else pass FD4 "the Question and Options bullets of all five decisions equal the printed ones"; fi
  if [ -n "$bad5" ]; then fail FD5 "answer or reason problems in:$bad5"; else pass FD5 "each Answer is one option label of its decision and each Owner reason is non-empty"; fi

  # FD6
  local nm dt dd nm_a dt_a drdate
  nm=$(line_val "- Decisions given by:" "$DC")
  dt=$(line_val "- Owner decision date:" "$DC")
  h3blk "$DC" "### Name" > "$TMP/n.rec"
  h3blk "$DC" "### Date" > "$TMP/d.rec"
  nm_a=$(line_val "- Answer:" "$TMP/n.rec")
  dt_a=$(line_val "- Answer:" "$TMP/d.rec")
  drdate=$(line_val "- Owner disposition date:" "$DR")
  m=""
  if [ -z "$(trim_ws "$nm")" ] || [ "$nm" != "$(trim_ws "$nm")" ]; then
    m="the name is empty or padded"
  elif [ "$nm_a" != "$nm" ] || [ "$(grep -c '^- Answer:' "$TMP/n.rec")" -ne 1 ]; then
    m="the name answer of the reply details differs from the header line"
  elif ! [[ "$dt" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ "$(date -u -d "$dt" +%F 2> /dev/null)" != "$dt" ]; then
    m="the date [$dt] is not a valid calendar date in the form YYYY-MM-DD"
  elif [ "$dt_a" != "$dt" ] || [ "$(grep -c '^- Answer:' "$TMP/d.rec")" -ne 1 ]; then
    m="the date answer of the reply details differs from the header line"
  elif ! [[ "$drdate" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    m="the owner disposition date of the disposition record is not a date"
  elif [[ "$dt" < "$drdate" ]]; then
    m="the date [$dt] is earlier than the owner disposition date of round 1 [$drdate]"
  elif [ "$(grep '^- Question:' "$TMP/n.rec")" != "- Question: $NAME_Q" ] || [ "$(grep '^- Question:' "$TMP/d.rec")" != "- Question: $DATE_Q" ]; then
    m="a question of the reply details differs from the printed one"
  fi
  if [ -n "$m" ]; then fail FD6 "$m"; else pass FD6 "name and date are complete, consistent and not earlier than the round-1 disposition date"; fi

  # FD7
  dd=$(h2sec "$DC" "What follows" | grep -v -x -F "$CLOSING_LINE" | grep -v '^$')
  if [ "$dd" = "$FOLLOWS_TEXT" ]; then pass FD7 "the What follows paragraph equals the printed one"; else fail FD7 "the What follows paragraph differs from the printed one"; fi

  if [ -n "$bad8" ]; then fail FD8 "finding problems in:$bad8"; else pass FD8 "the findings of every decision are findings with the disposition fix in the disposition record"; fi
}

# fd1_scan FILE [ALLOWED]: print the first self-containment problem of FILE, nothing when there is none. A
# hash-like token is allowed when it is one of the round-1 pins, the blob of the disposition record at HEAD or
# one of the words of ALLOWED (a string of tokens separated by spaces).
fd1_scan() {
  local f=$1 label re hit tok extra=${2:-}
  while IFS='|' read -r label re; do
    hit=$(grep -n -E -e "$re" "$f" | head -n1)
    if [ -n "$hit" ]; then
      echo "$label at line ${hit%%:*}"
      return 0
    fi
  done << 'PATTERNS'
drive-letter or home-directory path|(^|[^A-Za-z0-9])[A-Za-z]:[\\/]|/Users/|/home/|~/
web address|https?://
markdown link|\]\(
temporary directory|/tmp/
scratch, local-data or transcript reference|[Ss][Cc][Rr][Aa][Tt][Cc][Hh][Pp][Aa][Dd]|[Aa][Pp][Pp][Dd][Aa][Tt][Aa]|[Tt][Rr][Aa][Nn][Ss][Cc][Rr][Ii][Pp][Tt]
unfinished-text marker|(^|[^A-Za-z0-9])(TODO|FIXME|TBD|XXX)([^A-Za-z0-9]|$)
PATTERNS
  local drb allowed
  drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || drb=""
  allowed=" $A_BLOB $A_SHA $drb $extra "
  while IFS= read -r tok; do
    case "$allowed" in
      *" $tok "*) ;;
      *) echo "hash-like token [$tok] that is not one of the previously approved pins or the disposition record blob"; return 0 ;;
    esac
  done < <(grep -o -E '[0-9A-Fa-f]{7,}' "$f" | grep '[0-9]' | sort -u)
  return 0
}

# ---- stage edits -----------------------------------------------------------------------------------------

# rng FILE START END: the lines from the first line that begins with START up to, not including, the next line
# that begins with END.
rng() {
  awk -v s="$2" -v e="$3" '!on { if (index($0, s) == 1) { on = 1; print }; next } index($0, e) == 1 { exit } { print }' "$1"
}

# trow FILE START END ACTION PIPES: the first table row in the range whose first cell begins with the action
# name in backticks and that holds PIPES vertical bars (the transition tables and the tables of results differ
# in their column counts).
trow() {
  rng "$1" "$2" "$3" | awk -v a="| \`$4\` " -v n="$5" 'index($0, a) == 1 { t = $0; if (gsub(/\|/, "|", t) == n) { print; exit } }'
}

# exblock FILE ID: an acceptance example, from its title line to the line before the next example, heading or rule.
exblock() {
  awk -v h="**$2 — " 'on && /^(\*\*AE-|#|---$)/ { exit } index($0, h) == 1 { on = 1 } on' "$1"
}

# has TEXT FRAGMENT: the fragment is a substring of the text.
has() {
  [[ "$1" == *"$2"* ]]
}

# nchars TEXT: the number of characters (not bytes) of the text.
nchars() {
  printf '%s' "$1" | tr -d '\200-\277' | wc -c | tr -d ' '
}

# heads_of FILE: "line TAB number" for every numbered heading outside code fences.
heads_of() {
  awk '/^```/ { f = !f; next } !f && /^#+ [0-9]+(\.[0-9]+)*\.? / { n = $2; sub(/\.$/, "", n); print NR "\t" n }' "$1"
}

# reg_mask: the register with every field that is filled in later replaced by a marker.
reg_mask() {
  awk -v th="$REG_TBL_H" -v bl="^- ($REG_BULLETS_RE): " '
    /^## / { sec = $0; seen[sec] = 0; print; next }
    /^### / { print; next }
    sec == th && /^\| FG-/ { split($0, c, "|"); printf "|%s|%s|%s|%s|@|@|@|\n", c[2], c[3], c[4], c[5]; next }
    sec == "## Change details" && $0 ~ bl { l = $0; sub(/: .*$/, "", l); print l ": @"; next }
    sec == "## Change details" && /^  - / { next }
    sec == "## Normative lines removed or reworded" || sec == "## Findings whose quoted sentence an edit touched" {
      if ($0 != "" && !seen[sec]++) print "@"
      next
    }
    { print }
  '
}

PROB=""
bad() { if [ -z "$PROB" ]; then PROB=$1; fi; }

# ev GROUP LABEL: the value of a bullet of the entry of a group in the register.
ev() {
  awk -F'\t' -v g="$1" -v l="$2" '$1 == g && $2 == l { print substr($0, length($1) + length($2) + 3); exit }' "$TMP/reg.ent"
}

# F1 helpers: F1BAD collects the problems of FE1.
F1BAD=""
f1_note() { if [[ "; $F1BAD;" != *"; $1;"* ]]; then F1BAD="$F1BAD${F1BAD:+; }$1"; fi; }
# f1_gone GROUP NAME FUNCTION FRAGMENT: the fragment is in the place in the round-1 text and not in the new text.
f1_gone() {
  local old new
  old=$("$3" "$T1")
  new=$("$3" "$SP")
  if ! has "$old" "$4"; then
    f1_note "$1: internal: the old fragment [$4] is not in $2 of the round-1 text"
  elif has "$new" "$4"; then
    f1_note "$1: $2 still holds the old statement [$4]"
  fi
}
# f1_has GROUP NAME FUNCTION FRAGMENT: the fragment is in the place in the new text.
f1_has() {
  local new
  new=$("$3" "$SP")
  if [ -z "$new" ]; then
    f1_note "$1: $2 is not found"
  elif ! has "$new" "$4"; then
    f1_note "$1: $2 lacks [$4]"
  fi
}
# f1_same GROUP NAME FUNCTION: the place equals the place in the round-1 text.
f1_same() {
  local old new
  old=$("$3" "$T1")
  new=$("$3" "$SP")
  if [ -z "$old" ] || [ "$old" != "$new" ]; then f1_note "$1: $2 differs from the round-1 text"; fi
}
# f1_ex GROUP ID TAG WORDS...: the example exists with the tag and its Then line holds every word.
f1_ex() {
  local g=$1 id=$2 tag=$3 blk tl w
  shift 3
  blk=$(exblock "$SP" "$id")
  if [ -z "$blk" ]; then f1_note "$g: the example $id does not exist"; return 0; fi
  if ! printf '%s\n' "$blk" | grep -q -x -F -e "- Covers: $tag"; then f1_note "$g: $id lacks the tag [$tag]"; fi
  tl=$(printf '%s\n' "$blk" | grep '^Then ' | head -n1)
  for w in "$@"; do
    if ! has "$tl" "$w"; then f1_note "$g: the Then line of $id lacks [$w]"; fi
  done
}

# places of the checks FE1
p_wait8() { trow "$1" '### 8.3 ' '### 8.4 ' wait 7; }
p_waitres8() { trow "$1" '### 8.3 ' '### 8.4 ' wait 4; }

fe1_FG01() {
  f1_gone FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "or DoF determines failure"
  f1_has FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "Section 24.7"
  f1_has FG-01 "the wait row of the transition table of Section 8.3" p_wait8 "failed"
  f1_same FG-01 "the wait row of the table of results of Section 8.3" p_waitres8
  f1_ex FG-01 AE-295 'Section 8.3 (`wait`)' success failed
}

# para FILE START END KEY: the paragraph (the block of lines between blank lines) in the range that holds KEY.
para() {
  rng "$1" "$2" "$3" | awk -v k="$4" 'BEGIN { RS = "" } index($0, k) > 0 { print; exit }'
}
# f1_is GROUP NAME FUNCTION EXPECTED: the place equals the expected text.
f1_is() {
  local new
  new=$("$3" "$SP")
  if [ "$new" != "$4" ]; then f1_note "$1: $2 is [$new], expected [$4]"; fi
}
# f1_line GROUP NAME FUNCTION FRAGMENT...: one line of the place holds every fragment.
f1_line() {
  local g=$1 name=$2 fn=$3 l w ok
  shift 3
  while IFS= read -r l; do
    ok=1
    for w in "$@"; do
      if ! has "$l" "$w"; then ok=0; break; fi
    done
    if [ "$ok" -eq 1 ]; then return 0; fi
  done < <("$fn" "$SP")
  f1_note "$g: no line of $name holds all of [$*]"
}

# places of the checks FE1 (FG-02 to FG-06)
p_reopen8() { trow "$1" '### 8.3 ' '### 8.4 ' reopen 7; }
p_reopenres8() { trow "$1" '### 8.3 ' '### 8.4 ' reopen 4; }
p_reopenblk8() { p_reopenres8 "$1" | awk -F'|' '{ c = $(NF - 1); gsub(/^ +| +$/, "", c); print c }'; }
p_start8() { trow "$1" '### 8.3 ' '### 8.4 ' start 7; }
p_startres8() { trow "$1" '### 8.3 ' '### 8.4 ' start 4; }
p_start23() { trow "$1" '### 23.4 ' '### 23.5 ' start 5; }
p_cancel23() { trow "$1" '### 23.4 ' '### 23.5 ' cancel 5; }
p_para85() { para "$1" '### 8.5 ' '## 9. ' 'neither failed nor'; }
p_para84() { para "$1" '### 8.4 ' '### 8.5 ' 'DoF retains first priority'; }
p_lines83() { rng "$1" '### 8.3 ' '### 8.4 ' | grep -v '^|'; }
p_lines234() { rng "$1" '### 23.4 ' '### 23.5 ' | grep -v '^|'; }
p_after_hard242() {
  rng "$1" '### 24.2 ' '### 24.3 ' | awk 'BEGIN { RS = "" } f { print; exit } index($0, "A known hard failure therefore outranks") == 1 { f = 1 }'
}
p_rules242() {
  rng "$1" '### 24.2 ' '### 24.3 ' | awk 'index($0, "A known hard failure therefore outranks") == 1 { exit } index($0, "An action that evaluates gates decides from the results in this order") == 1 { on = 1 } on'
}
p_ask248() { para "$1" '### 24.8 ' '### 24.9 ' 'the `ask` action records a question without pausing the change'; }
p_realask() { awk 'index($0, "| Open questions as state |") == 1 { print; exit }' "$1"; }
p_realaskfull() { p_realask "$1" | awk -F'|' '{ print $(NF - 1) }'; }

fe1_FG02() {
  f1_gone FG-02 "the reopen row of the transition table of Section 8.3" p_reopen8 "wait when the new corrective scope's DoW determines a pause"
  f1_has FG-02 "the reopen row of the transition table of Section 8.3" p_reopen8 "DoW"
  f1_has FG-02 "the reopen row of the table of results of Section 8.3" p_reopenres8 "Definition of Wait"
  f1_is FG-02 "the blocked cell of the reopen row of the table of results of Section 8.3" p_reopenblk8 "Never."
  f1_ex FG-02 AE-296 'Section 8.3 (`reopen`)' rejected
}

fe1_FG03() {
  f1_gone FG-03 "the start row of the transition table of Section 23.4" p_start23 "finds no fail gate and no wait gate active"
  f1_has FG-03 "the start row of the transition table of Section 23.4" p_start23 "none of the steps 1 to 4"
  f1_has FG-03 "the start row of the transition table of Section 23.4" p_start23 "cannot be evaluated"
  f1_has FG-03 "the start row of the transition table of Section 8.3" p_start8 "cannot be evaluated"
  f1_has FG-03 "the start row of the table of results of Section 8.3" p_startres8 "cannot be evaluated"
  f1_has FG-03 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "start"
  f1_ex FG-03 AE-297 'Section 8.3 (`start`)' rejected
}

fe1_FG04() {
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "cancel"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "supersede"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "wait"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "fail"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "reopen"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "gate-not-evaluable"
  f1_has FG-04 "the paragraph of Section 24.2 after the paragraph on a known hard failure" p_after_hard242 "not_evaluable"
  f1_line FG-04 "the lines of Section 8.3 outside the tables" p_lines83 "Section 24.2" "cannot be evaluated"
  f1_line FG-04 "the lines of Section 23.4 outside the tables" p_lines234 "Section 24.2" "cannot be evaluated"
  f1_has FG-04 "the cancel row of the transition table of Section 23.4" p_cancel23 "cannot be evaluated"
  f1_has FG-04 "the paragraph of Section 8.4 on the priority of the Definition of Fail" p_para84 "cannot be evaluated"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "start"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "cancel"
  f1_has FG-04 "the paragraph of Section 8.5 on a gate that cannot be evaluated" p_para85 "Section 24.2"
  f1_ex FG-04 AE-298 'Section 8.3 (`cancel`)' cancelled
  f1_ex FG-04 AE-299 'Section 23.4 (`cancel`)' cancelled
}

fe1_FG05() {
  f1_has FG-05 "the rules of Section 24.2 and the paragraph that follows them" p_rules242 "Definition of Ready"
  f1_has FG-05 "the rules of Section 24.2 and the paragraph that follows them" p_rules242 "Section 8.3"
  f1_ex FG-05 AE-300 'Section 24.2 (full)' blocked
}

fe1_FG06() {
  f1_has FG-06 "the paragraph of Section 24.8 on the action ask" p_ask248 'the action `ask`'
  f1_has FG-06 "the paragraph of Section 24.8 on the action ask" p_ask248 "Section 25.1"
  f1_line FG-06 "the lines of Section 8.3 outside the tables" p_lines83 "approve" "ask" "answer" "adopt" "migrate" "Section 25.1"
  f1_gone FG-06 "the realization row Open questions as state" p_realask "The question is recorded in the state file"
  f1_has FG-06 "the full cell of the realization row Open questions as state" p_realaskfull "ask"
  f1_ex FG-06 AE-301 'Section 24.8 (full)' ask
}

# f1_nounless GROUP NAME FUNCTION: no line of the place that holds retry limit holds the word unless (either case).
f1_nounless() {
  if "$3" "$SP" | grep -F 'retry limit' | grep -q -i -w 'unless'; then f1_note "$1: a retry limit sentence of $2 holds the word unless"; fi
}

# places of the checks FE1 (FG-07 to FG-09)
p_open12() { rng "$1" '## 12. ' '### 12.1 '; }
p_new247() {
  rng "$1" '### 24.7 ' '### 24.8 ' | grep -v -x -F -f <(rng "$T1" '### 24.7 ' '### 24.8 ')
}
p_sec252() { rng "$1" '### 25.2 ' '### 25.3 '; }
p_sec224() { rng "$1" '### 22.4 ' '## 23. '; }
p_order22() { awk '/^### 22\.[0-9]+ / { printf "%s ", $2 }' "$1"; }
p_bullet221() { rng "$1" '### 22.1 ' '### 22.2 ' | grep -F '`guard`'; }
p_read234() { rng "$1" '### 23.4 ' '### 23.5 ' | grep -F 'are read-only'; }

fe1_FG07() {
  f1_has FG-07 "the opening of Section 12" p_open12 "retry limit"
  f1_has FG-07 "the opening of Section 12" p_open12 "soft"
  f1_has FG-07 "the opening of Section 12" p_open12 "Section 24.7"
  f1_line FG-07 "the opening of Section 12" p_open12 "retry limit" "closes the change as failed or records an override"
  f1_line FG-07 "the new lines of Section 24.7" p_new247 "retry limit" "human" "closes the change as failed or records an override"
  f1_nounless FG-07 "the opening of Section 12" p_open12
  f1_nounless FG-07 "the new lines of Section 24.7" p_new247
}

fe1_FG08() {
  f1_line FG-08 "Section 25.2" p_sec252 "MUST" "valid UTF-8" "zero byte"
  f1_gone FG-08 "Section 25.2" p_sec252 "an implementation SHOULD classify a file as text only when"
  f1_gone FG-08 "Section 25.2" p_sec252 "A content hash is therefore comparable only with a content hash that an implementation computed with the same decision"
  f1_ex FG-08 AE-302 'Section 25.2' text binary
}

fe1_FG09() {
  local w
  f1_is FG-09 "the order of the subsections of Section 22" p_order22 "22.1 22.2 22.3 22.4 "
  for w in 'guard' 'MUST NOT' 'Section 24.1' 'Section 24.3' 'Section 24.4' 'Section 24.5' 'Section 24.7' 'success' 'rejected' 'changed' \
    'history-inconsistent' 'anchor-missing' 'gates-changed' 'approval-stale' 'scope-violation' 'hard-failure-active'; do
    f1_has FG-09 "Section 22.4" p_sec224 "$w"
  done
  f1_has FG-09 "the reporting bullet of Section 22.1" p_bullet221 "Section 22.4"
  f1_has FG-09 "the sentence on the read-only actions in Section 23.4" p_read234 "Section 22.4"
  f1_ex FG-09 AE-303 'Section 22.4' success
  f1_ex FG-09 AE-304 'Section 22.4' rejected gates-changed
  f1_ex FG-09 AE-305 'Section 22.4' rejected
}

fe1() {
  local g n=0 fn
  F1BAD=""
  while IFS=$'\t' read -r g _ _ _ st _ _; do
    [ "$st" = drafted ] || continue
    n=$((n + 1))
    fn="fe1_${g//-/}"
    if declare -F "$fn" > /dev/null; then "$fn"; else f1_note "$g: no FE1 checks are defined for this group"; fi
  done < "$TMP/reg.rows"
  if [ -n "$F1BAD" ]; then fail FE1 "$F1BAD"; else pass FE1 "for each of the $n drafted groups the old statement is gone, the new facts are present and the examples exist with their tags"; fi
}

# sent22 FILE: the sentence of Section 22.2 that lists the actions which can answer blocked.
sent22() {
  rng "$1" '### 22.2 ' '### 22.3 ' | awk '{ i = index($0, "Only the actions that complete"); j = index($0, " Every other action answers"); if (i > 0 && j > i) { print substr($0, i, j - i); exit } }'
}
# lastcells FILE START END: the last cell of every row of the table of results in the range (rows of three columns).
lastcells() {
  rng "$1" "$2" "$3" | awk '{ t = $0; if (gsub(/\|/, "|", t) == 4 && $0 !~ /^\|[-|]+\|$/) { n = split($0, c, "|"); print c[n - 1] } }'
}
# realrow FILE: the realization row of the result blocked.
realrow() {
  awk 'index($0, "| The result `blocked` |") == 1 { print; exit }' "$1"
}

fe2() {
  local a b id
  PROB=""
  a=$(sent22 "$T1"); b=$(sent22 "$SP")
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the sentence of Section 22.2 that lists the actions which can answer blocked is not the round-1 sentence"; fi
  a=$(lastcells "$T1" '### 8.3 ' '### 8.4 '); b=$(lastcells "$SP" '### 8.3 ' '### 8.4 ')
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "a blocked cell (the last cell) of the table of results of Section 8.3 differs from the round-1 text"; fi
  a=$(lastcells "$T1" '### 23.4 ' '### 23.5 '); b=$(lastcells "$SP" '### 23.4 ' '### 23.5 ')
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "a blocked cell (the last cell) of the table of results of Section 23.4 differs from the round-1 text"; fi
  a=$(realrow "$T1"); b=$(realrow "$SP")
  if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the realization row of the result blocked differs from the round-1 text"; fi
  for id in AE-259 AE-287; do
    a=$(exblock "$T1" "$id"); b=$(exblock "$SP" "$id")
    if [ -z "$a" ] || [ "$a" != "$b" ]; then bad "the example $id differs from the round-1 text"; fi
  done
  if [ -n "$PROB" ]; then fail FE2 "$PROB"; else pass FE2 "the sentence of Section 22.2, the blocked cells of both tables of results, the realization row of the result blocked and the examples AE-259 and AE-287 equal the round-1 text"; fi
}

# fe_diff: the difference round-1 text to new text as two files, $TMP/d.add ("line TAB text" of the new text) and
# $TMP/d.del ("position TAB text"; the position is the line of the new text at or before the removal).
fe_diff() {
  : > "$TMP/d.add"
  : > "$TMP/d.del"
  diff -U0 "$T1" "$SP" > "$TMP/spec.diff"
  [ "$?" -le 1 ] || { echo "cannot compare the specification with the round-1 text" >&2; exit 2; }
  awk -v add="$TMP/d.add" -v del="$TMP/d.del" '
    /^@@ / { h = $0; sub(/^@@ -[0-9,]+ \+/, "", h); split(h, p, /[ ,]/); c = p[1] + 0; nl = c; inh = 1; next }
    !inh { next }
    /^\+/ { print nl "\t" substr($0, 2) >> add; nl++; next }
    /^-/ { print c "\t" substr($0, 2) >> del }
  ' "$TMP/spec.diff"
}

# listed_sections: the section numbers of the Sections cells of the register, one per line.
listed_sections() {
  awk -F'\t' '$6 != "-" { n = split($6, a, ","); for (i = 1; i <= n; i++) { s = a[i]; gsub(/ /, "", s); if (s != "") print s } }' "$TMP/reg.rows"
}

fe3() {
  local id sev q ln
  PROB=""
  if ! cmp -s <(head -n8 "$T1") <(head -n8 "$SP"); then bad "the first eight lines of the specification (the header) differ from the round-$((ROUND - 1)) text"; fi
  # the quoted sentences of the findings that were not dispositioned
  h2sec "$RG" "Findings whose quoted sentence an edit touched" | grep -o -E "^- $FPFX-[A-Z]-[0-9]{3} :: .+" | cut -d' ' -f2 > "$TMP/touched.ids"
  undisp > "$TMP/undisp.tsv"
  if [ "$(wc -l < "$TMP/undisp.tsv" | tr -d ' ')" -ne "$NUNDISP" ]; then bad "the review note does not hold $NUNDISP findings without a disposition"; fi
  if [ "$ROUND" -ge 3 ]; then base_ids > "$TMP/base.ids"; else : > "$TMP/base.ids"; fi
  while IFS=$'\t' read -r id sev q; do
    # Profile 5: a quoted sentence that the text of round 4 does not hold (a quote that differs from the text in
    # letter case, for example) cannot have been removed by an edit and is not looked up.
    if [ "$ROUND" -ge 5 ] && ! grep -q -F -e "$q" "$T1"; then continue; fi
    if [ -n "$q" ] && ! grep -q -F -e "$q" "$SP" && ! grep -q -x -F -e "$id" "$TMP/touched.ids" && ! grep -q -x -F -e "$id" "$TMP/base.ids"; then
      bad "the quoted sentence of the undispositioned finding $id is no longer in the specification and the register lists no reason"
    fi
  done < "$TMP/undisp.tsv"
  # the changed paths
  { git diff --name-only --no-renames "$BASE...HEAD"; git diff --name-only --no-renames HEAD; git ls-files --others --exclude-standard; } 2> /dev/null | sort -u > "$TMP/paths.txt"
  while IFS= read -r ln; do
    [ -n "$ln" ] || continue
    case "$ln" in
      "$SPEC"|.planning/*) ;;
      *) bad "the path [$ln] changed since the base and is neither the specification nor under .planning/" ;;
    esac
  done < "$TMP/paths.txt"
  # a tab in an added line
  if awk -F'\t' 'NF > 2 { found = 1 } END { exit found ? 0 : 1 }' "$TMP/d.add"; then
    bad "an added line of the specification holds a tab"
  fi
  # every changed line lies inside a listed section
  heads_of "$SP" > "$TMP/heads.tsv"
  listed_sections > "$TMP/listed.txt"
  cat "$TMP/d.add" "$TMP/d.del" | awk -F'\t' '
    FILENAME == hf { hl[++nh] = $1; hn[nh] = $2; next }
    FILENAME == lf { ok[$1] = 1; next }
    $2 ~ /^[ ]*$/ { next }
    {
      n = $1 + 0; s = "0"
      for (i = nh; i >= 1; i--) if (hl[i] <= n) { s = hn[i]; break }
      if (!(s in ok)) { print "line " n " lies in section " s; exit }
    }
  ' hf="$TMP/heads.tsv" lf="$TMP/listed.txt" "$TMP/heads.tsv" "$TMP/listed.txt" - > "$TMP/fe3.sec"
  if [ -s "$TMP/fe3.sec" ]; then bad "a changed line is outside the sections listed in the register ($(head -n1 "$TMP/fe3.sec"))"; fi
  if [ -n "$PROB" ]; then fail FE3 "$PROB"; else pass FE3 "the header and the $NUNDISP undispositioned findings are untouched, only the specification and .planning/ changed, no added line holds a tab, and every changed line lies in a listed section"; fi
}

# csub TEXT N: the first N characters of the text.
csub() {
  printf '%s' "$1" | awk -v n="$2" '{ cnt = 0; for (i = 1; i <= length($0); i++) { b = substr($0, i, 1); if (b !~ /[\200-\277]/) { cnt++; if (cnt > n) { print substr($0, 1, i - 1); next } } } print $0 }'
}

fe4() {
  local txt key k
  PROB=""
  h2sec "$RG" "Normative lines removed or reworded" | grep -E '^- .* :: .+' > "$TMP/fe4.bullets"
  : > "$TMP/fe4.keys"
  while IFS=$'\t' read -r _ txt; do
    if printf '%s\n' "$txt" | grep -q -E '(^|[^A-Za-z])(MUST|SHOULD|MAY)([^A-Za-z]|$)'; then
      key=$(csub "$txt" 60)
      printf '%s\n' "$key" >> "$TMP/fe4.keys"
      if ! K="- $key :: " awk 'index($0, ENVIRON["K"]) == 1 { f = 1 } END { exit f ? 0 : 1 }' "$TMP/fe4.bullets"; then
        bad "a removed line with MUST, SHOULD or MAY has no register line with a reason: [$key]"
      fi
    fi
  done < "$TMP/d.del"
  while IFS= read -r k; do
    [ -n "$k" ] || continue
    key=${k#- }
    key=${key%% :: *}
    if ! grep -q -x -F -e "$key" "$TMP/fe4.keys"; then echo "WARN FE4 a register line matches no removed line: [$key]"; fi
  done < "$TMP/fe4.bullets"
  if [ -n "$PROB" ]; then fail FE4 "$PROB"; else pass FE4 "every removed line with MUST, SHOULD or MAY has a register line with a reason"; fi
}

fe5() {
  local g kind st secs exs v frag lab lim tok id n=0 top expect last want
  local -a toks
  PROB=""
  # the layout and the encoding
  reg_mask < "$RG" > "$TMP/mask.rg"
  print_register_skeleton | reg_mask > "$TMP/mask.sk"
  if ! cmp -s "$TMP/mask.rg" "$TMP/mask.sk"; then
    bad "the layout differs from the printed skeleton (first difference: $(diff "$TMP/mask.sk" "$TMP/mask.rg" | grep '^[<>]' | head -n1 | cut -c1-80))"
  fi
  v=$(enc1 "$RG"); if [ -z "$v" ]; then v=$(enc2 "$RG"); fi
  if [ -n "$v" ]; then bad "$v"; fi
  if [ -z "$PROB" ]; then v=$(fd1_scan "$RG"); if [ -n "$v" ]; then bad "self-containment: $v"; fi; fi
  if [ "$(wc -l < "$TMP/reg.rows" | tr -d ' ')" -ne "$NCHG" ]; then bad "the table does not hold $NCHG_W rows"; fi
  heads_of "$SP" | cut -f2 > "$TMP/headnums.txt"
  : > "$TMP/ids.all"
  while IFS=$'\t' read -r g _ _ kind st secs exs; do
    case "$st" in
      drafted) n=$((n + 1)) ;;
      pending) if [ "$COMPLETE" -eq 1 ]; then bad "$g is not drafted (--complete needs all $NCHG_W)"; fi; continue ;;
      *) bad "$g: the Status cell is [$st], expected pending or drafted"; continue ;;
    esac
    if [ "$secs" = "-" ] || [ -z "$secs" ]; then bad "$g: the Sections cell is empty"; fi
    for lab in "${REG_BULLETS[@]}"; do
      v=$(ev "$g" "$lab")
      if [ -z "$v" ] || [ "$v" = pending ] || has "$v" "$FILL"; then bad "$g: the bullet [$lab] is not filled"; fi
    done
    if [ "$ROUND" -eq 2 ]; then
      for lab in "What changed:300" "Why:200" "My choice:450"; do
        v=$(ev "$g" "${lab%:*}"); lim=${lab##*:}
        if [ "$(nchars "$v")" -gt "$lim" ]; then bad "$g: [${lab%:*}] is longer than $lim characters"; fi
        case "$v" in
          *"Section "*|*"AE-"*|*"|"*) bad "$g: [${lab%:*}] holds a section number, an example id or a vertical bar" ;;
        esac
      done
      v=$(ev "$g" "My choice")
      case "$kind" in
        repair) case "$v" in "none:"*) ;; *) bad "$g: a repair must give My choice as [none:] and the reason" ;; esac ;;
        "my choice")
          case "$v" in "none"*) bad "$g: a choice between readings must not give My choice as none" ;; esac
          if ! has "$v" "other"; then bad "$g: My choice does not name the other readings"; fi ;;
      esac
      if [ "$g" = FG-09 ]; then
        for tok in '(1)' '(2)' '(3)' '(4)'; do
          if ! has "$v" "$tok"; then bad "FG-09: My choice lacks the marker $tok of the numbered list of my own readings"; fi
        done
      fi
    else
      for lab in "What changed:300" "Why:200"; do
        v=$(ev "$g" "${lab%:*}"); lim=${lab##*:}
        if [ "$(nchars "$v")" -gt "$lim" ]; then bad "$g: [${lab%:*}] is longer than $lim characters"; fi
        case "$v" in
          *"Section "*|*"AE-"*|*"|"*) bad "$g: [${lab%:*}] holds a section number, an example id or a vertical bar" ;;
        esac
      done
      want=$(fg_kind "$g")
      if [ "$kind" != "$want" ]; then bad "$g: the Kind cell is [$kind], expected ${want:-a change of this round}"; fi
    fi
    for lab in Before After; do
      v=$(ev "$g" "$lab")
      if [ "$lab" = Before ] && [ "$v" = "none (new text)" ]; then continue; fi
      case "$v" in
        \"*\") ;;
        *) bad "$g: [$lab] is not one quoted fragment"; continue ;;
      esac
      frag=${v#\"}; frag=${frag%\"}
      if [ -z "$frag" ] || [ "$(nchars "$frag")" -gt 300 ]; then bad "$g: [$lab] is empty or longer than 300 characters"; continue; fi
      if [ "$lab" = Before ]; then
        grep -q -F -e "$frag" "$T1" || bad "$g: the Before fragment is not a part of a line of the round-$((ROUND - 1)) text"
      else
        grep -q -F -e "$frag" "$SP" || bad "$g: the After fragment is not a part of a line of the new text"
      fi
    done
    IFS=',' read -r -a toks <<< "$secs"
    for tok in "${toks[@]}"; do
      tok=${tok// /}
      grep -q -x -F -e "$tok" "$TMP/headnums.txt" || bad "$g: the Sections cell names [$tok], which is no heading number of the specification"
    done
    if [ "$exs" != "-" ]; then
      IFS=',' read -r -a toks <<< "$exs"
      for tok in "${toks[@]}"; do
        id=${tok// /}
        printf '%s\n' "$id" >> "$TMP/ids.all"
        v=$(exblock "$SP" "$id")
        if [ -z "$v" ] || ! printf '%s\n' "$v" | grep -q '^- Covers: '; then bad "$g: the example $id does not exist with a Covers line"; fi
        if [ "$(grep -c -w -e "$id" "$SP")" -lt 2 ]; then bad "$g: the example $id is not cited"; fi
      done
    fi
  done < "$TMP/reg.rows"
  # the examples run on from the first new id without a gap or a repeat, and the highest id of the specification
  # ends the run
  sort -t- -k2 -n "$TMP/ids.all" > "$TMP/ids.sorted"
  expect=$EX_FIRST
  last=$((EX_FIRST - 1))
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    if [ "$id" != "AE-$expect" ]; then bad "the example ids of the register do not run on from AE-$EX_FIRST without a gap or a repeat (expected AE-$expect, found $id)"; break; fi
    last=$expect
    expect=$((expect + 1))
  done < "$TMP/ids.sorted"
  top=$(grep -o '^\*\*AE-[0-9]*' "$SP" | sed 's/\*\*AE-//' | sort -n | tail -n1)
  if [ "$top" != "$last" ]; then bad "the highest example id of the specification is AE-$top, but the register ends its run at AE-$last"; fi
  if [ "$COMPLETE" -eq 1 ]; then
    if [ "$n" -ne "$NCHG" ]; then bad "not all $NCHG_W groups are drafted"; fi
    cut -f3 "$TMP/reg.rows" | grep -o -E "$FPFX-[A-Z]-[0-9]{3}" | sort -u > "$TMP/fnd.reg"
    drec_fix_ids | sort -u > "$TMP/fnd.fix"
    if ! cmp -s "$TMP/fnd.reg" "$TMP/fnd.fix"; then bad "the Findings cells of the register do not cover exactly the findings with the disposition fix"; fi
  fi
  if [ -n "$PROB" ]; then fail FE5 "$PROB"; else pass FE5 "the register is intact and its $n drafted entries are consistent with the text"; fi
}

fe6() {
  local args=(--final) out rc last
  if [ "$SPECFILE" != "$SPEC" ]; then args+=(--file "$SPECFILE"); fi
  out=$(bash "$CHK2" "${args[@]}" 2>&1)
  rc=$?
  last=$(printf '%s\n' "$out" | tail -n1)
  if [ "$rc" -eq 0 ] && [ "$last" = "RESULT: PASS" ]; then
    pass FE6 "the Phase 2 check with --final ends RESULT: PASS"
  else
    fail FE6 "the Phase 2 check with --final does not pass: $(printf '%s\n' "$out" | grep '^FAIL' | head -n3 | tr '\n' ';' | cut -c1-300)"
  fi
}

# reg_load: read the register into $TMP/reg.rows (one line per group, seven tab-separated cells of the table) and
# $TMP/reg.ent (group, label and value of every bullet of the entries).
reg_load() {
  : > "$TMP/reg.rows"
  : > "$TMP/reg.ent"
  awk -v rows="$TMP/reg.rows" -v ent="$TMP/reg.ent" -v th="$REG_TBL_H" -v bl="^- ($REG_BULLETS_RE): " '
    function trim(s) { sub(/^ +/, "", s); sub(/ +$/, "", s); return s }
    /^## / { sec = $0; cur = ""; next }
    /^### FG-/ { cur = $2; next }
    sec == th && /^\| FG-/ {
      split($0, c, "|")
      print trim(c[2]) "\t" trim(c[3]) "\t" trim(c[4]) "\t" trim(c[5]) "\t" trim(c[6]) "\t" trim(c[7]) "\t" trim(c[8]) >> rows
      next
    }
    sec == "## Change details" && cur != "" && $0 ~ bl {
      l = $0; sub(/^- /, "", l); v = l; sub(/^[^:]*: /, "", v); sub(/:.*$/, "", l)
      print cur "\t" l "\t" v >> ent
    }
  ' "$RG"
}

# fe7: profiles 3 and 4. For each drafted entry the Options bullet equals the labels that
# --print-decision-questions prints for its decision, joined by " | ", the Owner decision equals exactly one of
# them, the Owner reason is non-empty and the Channel is the fixed sentence. For an entry of the kind repair
# (profile 4) each of the four bullets Options, Owner decision, Owner reason and Channel equals the fixed
# no-choice sentence.
fe7() {
  local g st od lab want v n=0 ok
  PROB=""
  while IFS=$'\t' read -r g _ _ _ st _ _; do
    [ "$st" = drafted ] || continue
    n=$((n + 1))
    if [ "$(fg_kind "$g")" = repair ]; then
      for lab in "Options" "Owner decision" "Owner reason" "Channel"; do
        v=$(ev "$g" "$lab")
        if [ "$v" != "$NOCHOICE_TEXT" ]; then bad "$g: the bullet [$lab] is not the fixed sentence for a change with no design choice"; fi
      done
      continue
    fi
    case "$g" in
      FG-10) od=OD-1 ;;
      FG-11) od=OD-2 ;;
      FG-12) od=OD-3 ;;
      FG-13) od=OD-4 ;;
      FG-14) od=OD-5 ;;
      FG-16) od=OD-6 ;;
      FG-17) od=OD-7 ;;
      FG-18) od=OD-8 ;;
      FG-19) od=OD-9 ;;
      FG-24) od=OD-10 ;;
      FG-25) od=OD-11 ;;
      FG-26) od=OD-12 ;;
      FG-28) od=OD-13 ;;
      *) bad "$g: no decision belongs to this change"; continue ;;
    esac
    want=$(od_labels "$od" | awk 'NR > 1 { printf " | " } { printf "%s", $0 }')
    v=$(ev "$g" "Options")
    if [ "$v" != "$want" ]; then bad "$g: the Options bullet is not the labels that were offered for $od [$want]"; fi
    v=$(ev "$g" "Owner decision")
    ok=0
    while IFS= read -r lab; do
      if [ "$v" = "$lab" ]; then ok=1; fi
    done < <(od_labels "$od")
    if [ "$ok" -eq 0 ]; then bad "$g: the Owner decision [$v] is not one of the labels that were offered for $od"; fi
    v=$(ev "$g" "Owner reason")
    if [ -z "$(trim_ws "$v")" ] || [ "$v" = pending ] || has "$v" "$FILL"; then bad "$g: the Owner reason is empty"; fi
    v=$(ev "$g" "Channel")
    if [ "$v" != "$CHANNEL_TEXT" ]; then bad "$g: the Channel bullet is not the fixed sentence"; fi
  done < "$TMP/reg.rows"
  if [ -n "$PROB" ]; then fail FE7 "$PROB"; else pass FE7 "for each of the $n drafted entries the Options are the labels that were offered, the Owner decision is one of them, the Owner reason is given and the Channel is the fixed sentence"; fi
}

# ---- stage dispositions: DA1 to DA5 on the disposition addendum (profile 5) ----------------------------------

# ad_blocks: the blocks of the addendum, one line per block: "#id TAB status TAB =question TAB =disposition TAB =reason".
ad_blocks() {
  h2sec "$AD" "Findings dispositioned by the owner" | awk '
    function trim(s) { sub(/^[ \t]+/, "", s); sub(/[ \t]+$/, "", s); return s }
    function val(l, p) { return trim(substr(l, length(p) + 1)) }
    function flush() {
      if (id == "") return
      if (bad == "" && st < 3) bad = "the block lacks the bullets Question, Disposition, Owner reason in that order"
      print "#" id "\t" (bad == "" ? "ok" : bad) "\t=" q "\t=" d "\t=" trim(r)
    }
    /^### / { flush(); id = trim(substr($0, 5)); q = ""; d = ""; r = ""; bad = ""; st = 0; next }
    id == "" { next }
    st == 3 { r = r " " $0; next }
    NF == 0 { next }
    st == 0 { if (index($0, "- Question: ") == 1) { q = $0; st = 1 } else { bad = "the first bullet is not [- Question: ]"; st = 9 }; next }
    st == 1 { if (index($0, "- Disposition:") == 1) { d = val($0, "- Disposition:"); st = 2 } else { bad = "the second bullet is not [- Disposition: ]"; st = 9 }; next }
    st == 2 { if (index($0, "- Owner reason:") == 1) { r = val($0, "- Owner reason:"); st = 3 } else { bad = "the third bullet is not [- Owner reason: ]"; st = 9 }; next }
    END { flush() }
  '
}

da_checks() {
  local m l n id st q d r exp_q rsha_calc drb drdate name_a date_a given_by date_line dd
  local -a rd=()

  # DA1
  if [ "$AD_OK" -eq 0 ]; then
    fail DA1 "the addendum cannot be read"
    return 0
  fi
  m=$(enc1 "$AD")
  if [ -z "$m" ]; then m=$(enc2 "$AD"); fi
  if [ -z "$m" ] && grep -q -F "$FILL" "$AD"; then m="a fill marker is left in a field (line $(grep -n -F "$FILL" "$AD" | head -n1 | cut -d: -f1))"; fi
  if [ -z "$m" ]; then m=$(fd1_scan "$AD" "$(tbl_tokens < "$AD")"); fi
  if [ -z "$m" ]; then
    if [ "$(head -n1 "$AD")" != "$AD_H1" ]; then
      m="the first line is not the H1 [$AD_H1]"
    elif [ "$(grep -c '^- Owner disposition date:' "$AD")" -ne 1 ]; then
      m="the addendum does not hold exactly one line [- Owner disposition date:]"
    elif [ "$(awk '/^```/ { f = !f; next } !f && /^## / { print }' "$AD" | tr '\n' '|')" != "## Findings dispositioned by the owner|## Reply details|## What follows|" ]; then
      m="the H2 headings are not the three expected ones in order"
    elif [ "$(tail -n1 "$AD")" != "$CLOSING_LINE" ] || [ "$(grep -c -x -F "$CLOSING_LINE" "$AD")" -ne 1 ]; then
      m="the closing line is not the last line, once"
    fi
  fi
  if [ -n "$m" ]; then fail DA1 "$m"; else pass DA1 "the addendum is clean text without fill markers, passes the scan and has the expected structure"; fi

  # DA2
  m=""
  parse_pins "$AD" "$TMP/ad.pins"
  if [ "$(awk -F'\t' '{ printf "%s|", $1 }' "$TMP/ad.pins")" != "$(printf '%s|' "${AD_LABELS[@]}")" ]; then
    m="the table rows are not the expected rows in the expected order"
  fi
  if [ -z "$m" ]; then
    for l in "${AD_COPIED[@]}" "Reports SHA-256"; do
      if [ "$(pin_raw "$TMP/ad.pins" "$l")" != "$(pin_raw "$TMP/dr.pins" "$l")" ]; then m="the row [$l] differs from the disposition record"; break; fi
    done
  fi
  if [ -z "$m" ] && [ "$(pin_raw "$TMP/ad.pins" "Review note file")" != "\`$NOTE_DEFAULT\`" ]; then m="Review note file is not \`$NOTE_DEFAULT\`"; fi
  if [ -z "$m" ]; then
    rsha_calc=$(reports_sha)
    if [ "$(pin_raw "$TMP/ad.pins" "Reports SHA-256")" != "\`$rsha_calc\`" ]; then m="Reports SHA-256 is not the hash of the Reports section of the review note ($rsha_calc)"; fi
  fi
  if [ -z "$m" ] && [ "$(pin_raw "$TMP/ad.pins" "Disposition record file")" != "\`$DREC_DEFAULT\`" ]; then m="Disposition record file is not \`$DREC_DEFAULT\`"; fi
  if [ -z "$m" ]; then
    drb=$(git rev-parse --verify --quiet "HEAD:$DREC_DEFAULT") || drb=""
    if [ "$(pin_raw "$TMP/ad.pins" "Disposition record blob")" != "\`$drb\`" ]; then m="Disposition record blob is not the blob of the disposition record at HEAD"; fi
  fi
  if [ -z "$m" ]; then
    for l in "Dispositions given by" "Owner reply" "Check results"; do
      if [ -z "$(pin_raw "$TMP/ad.pins" "$l")" ]; then m="the row [$l] is empty"; break; fi
    done
  fi
  if [ -n "$m" ]; then fail DA2 "$m"; else pass DA2 "the pin rows, the Reports SHA-256, the disposition record file and blob equal the records and the note, and the owner rows are filled"; fi

  # DA3
  m=""
  ad_blocks > "$TMP/ad.blocks"
  n=$(wc -l < "$TMP/ad.blocks" | tr -d ' ')
  undisp_skip "" | cut -f1 > "$TMP/ad.avail"
  awk '/^### / { print $2 }' "$DR" > "$TMP/ad.drids"
  fg5_ids | sort -u > "$TMP/ad.static"
  if [ -n "$(h2sec "$AD" "Findings dispositioned by the owner" | awk '/^### / { exit } NF')" ]; then
    m="the section Findings dispositioned by the owner holds text before its first block"
  fi
  while [ -z "$m" ] && IFS=$'\t' read -r id st q d r; do
    id=${id#\#}; q=${q#=}; d=${d#=}; r=${r#=}
    if grep -q -x -F -e "$id" "$TMP/ad.drids"; then m="block $id: the disposition record of round $ADD_RND already dispositions this finding"; break; fi
    if ! grep -q -x -F -e "$id" "$TMP/ad.avail"; then m="block $id: no finding of the review note without a disposition has this id"; break; fi
    if [ "$st" != ok ]; then m="block $id: $st"; break; fi
    exp_q=$(disp_q "$id")
    if [ -z "$exp_q" ] || [ "$q" != "$exp_q" ]; then m="block $id: the question differs from the one that the review check script prints"; break; fi
    case "$d" in fix|accept|defer|reject) ;; *) m="block $id: the disposition [${d:0:40}] is not one of fix, accept, defer, reject"; break ;; esac
    if [ -z "$r" ]; then m="block $id: the owner reason is empty"; break; fi
    if [ "$d" != fix ] && [ "$r" = "none given" ]; then m="block $id: the disposition $d needs a reason, [none given] is not one"; break; fi
    if [ "$d" = fix ] && ! grep -q -x -F -e "$id" "$TMP/ad.static"; then m="block $id: the disposition fix has no change in the plan of round $ROUND (the plan is revised outside this script)"; break; fi
  done < "$TMP/ad.blocks"
  if [ -z "$m" ]; then
    cut -f1 "$TMP/ad.blocks" | sed 's/^#//' > "$TMP/ad.ids"
    if [ -n "$(sort "$TMP/ad.ids" | uniq -d)" ]; then
      m="the block $(sort "$TMP/ad.ids" | uniq -d | head -n1) occurs twice"
    elif ! cmp -s "$TMP/ad.ids" <(grep -x -F -f "$TMP/ad.ids" "$TMP/ad.avail"); then
      m="the blocks are not in the order of the findings table of the review note"
    else
      for id in ${AD_DEFAULT_IDS//,/ }; do
        if ! grep -q -x -F -e "$id" "$TMP/ad.ids"; then m="the block of $id is missing"; break; fi
      done
    fi
  fi
  if [ -n "$m" ]; then fail DA3 "$m"; else pass DA3 "the $n blocks are findings without a disposition in table order, each with the printed question, one of fix, accept, defer, reject and a reason, and every fix has a change"; fi

  # DA4
  m=""
  mapfile -t rd < <(h2sec "$AD" "Reply details" | grep -v '^[[:space:]]*$')
  given_by=$(pin_raw "$TMP/ad.pins" "Dispositions given by")
  date_line=$(line_val "- Owner disposition date:" "$AD")
  drdate=$(line_val "- Owner disposition date:" "$DR")
  if [ "${#rd[@]}" -ne 6 ] || [ "${rd[0]}" != "### Name" ] || [ "${rd[1]}" != "- Question: $AD_NAME_Q" ] || [ "${rd[3]}" != "### Date" ] || [ "${rd[4]}" != "- Question: $AD_DATE_Q" ] \
    || [[ "${rd[2]}" != "- Answer: "* ]] || [[ "${rd[5]}" != "- Answer: "* ]]; then
    m="the section Reply details is not the blocks Name and Date, each with the fixed question and a one-line answer"
  else
    name_a=${rd[2]#- Answer: }
    date_a=${rd[5]#- Answer: }
    if [ -z "$(trim_ws "$name_a")" ] || [ "$name_a" != "$(trim_ws "$name_a")" ]; then
      m="the name is empty or padded"
    elif [ "$name_a" != "$given_by" ]; then
      m="the name differs from the row Dispositions given by"
    elif ! [[ "$date_a" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ "$(date -u -d "$date_a" +%F 2> /dev/null)" != "$date_a" ]; then
      m="the date [${date_a:0:30}] is not a valid calendar date in the form YYYY-MM-DD"
    elif [ "$date_a" != "$date_line" ]; then
      m="the date answer differs from the line [- Owner disposition date:]"
    elif ! [[ "$drdate" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      m="the owner disposition date of the disposition record of round $ADD_RND is not a date"
    elif [[ "$date_a" < "$drdate" ]]; then
      m="the date $date_a is earlier than the owner disposition date of the record of round $ADD_RND ($drdate)"
    fi
  fi
  if [ -z "$m" ] && [ -z "$(trim_ws "$(pin_raw "$TMP/ad.pins" "Owner reply")")" ]; then m="the Owner reply row is empty"; fi
  if [ -n "$m" ]; then fail DA4 "$m"; else pass DA4 "the name equals Dispositions given by, the date is a valid calendar date equal to the date line and not earlier than $drdate"; fi

  # DA5
  dd=$(h2sec "$AD" "What follows" | grep -v -x -F "$CLOSING_LINE" | grep -v '^$')
  if [ "$dd" != "$AD_FOLLOWS_TEXT" ]; then
    fail DA5 "the section What follows differs from the printed text"
  elif [ "$(tail -n1 "$AD")" != "$CLOSING_LINE" ] || [ "$(grep -c -x -F "$CLOSING_LINE" "$AD")" -ne 1 ]; then
    fail DA5 "the closing line is not the last line, once"
  else
    pass DA5 "the section What follows equals the printed text and the closing line ends the addendum"
  fi
}

edits_stage() {
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then echo "the result blob of the approval record is not 40 lowercase hexadecimal digits" >&2; exit 2; fi
  git cat-file blob "$A_BLOB" > "$T1" 2> /dev/null || { echo "the round-$((ROUND - 1)) text cannot be read from the repository" >&2; exit 2; }
  reg_load
  fe_diff
  if [ "$ADD_RND" -gt 0 ]; then da_checks; fi
  if [ "$ROUND" -eq 2 ]; then
    fe1
    fe2
  fi
  fe3
  fe4
  fe5
  fe6
  if [ "$ROUND" -ge 3 ]; then fe7; fi
}

# ---- the owner approval of the exact new text --------------------------------------------------------------

AP_H1='# Owner approval packet, fix round: proposed normative method specification'
AR_H1='# Owner approval record, fix round: proposed normative method specification'
AP_PENDING='- Owner approval: pending'
AP_RECORDED='- Owner approval: recorded in the owner approval record'
AP_CLOSING='This packet is evidence only. It does not change the reviewed file.'
AR_CLOSING='This record is evidence only. It does not change the reviewed file.'
OPT_APPROVE='Approve exact text'
OPT_APPROVE_DESC='The text is approved as it stands and goes to the limited independent review that the packet describes.'
OPT_CHANGES='Request changes'
OPT_CHANGES_DESC='Nothing is approved; you say what to change.'
NOT_ASKED='None. (not asked, because the text was approved)'
AQ_HEADS=(Approval Changes Name Date)
AP_FOLLOWS_1='If you approve, the text goes to an independent review by a reviewer that is not the Requestor. That review is limited: it has one pass over the header and Sections 1 to 8, one pass over Sections 9 to 22 and one pass over the whole text read across sections. Sections 23, 24 and 25 have no pass of their own and are read only by the pass over the whole text. Any later edit of the specification voids the approval.'
AP_FOLLOWS_2='If you request changes, nothing is approved, the text is edited for them, the packet is printed again and you are asked again.'
AP_FOLLOWS_3='The tick of the requirement for owner approval from the first round is not changed by any plan and rests, for this text, on the record that follows this packet.'
if [ "$ROUND" -ge 3 ]; then
  AP_H1="# Owner approval packet, fix round $ROUND: proposed normative method specification"
  AR_H1="# Owner approval record, fix round $ROUND: proposed normative method specification"
  AP_FOLLOWS_1='If you approve, the text goes to an independent review by a reviewer that is not the Requestor. Before anything is sent, you decide which parts of the text that review reads, with the figures of what changed where, and you consent to the exact run. Any later edit of the specification voids the approval.'
fi
# Profile 4: the reading of a change for which no decision was asked (the kind repair).
AP_NOASK_CELL='no decision asked: the finding names the fix'
AP_NOASK_BULLET='none asked; the finding leaves no design choice'

# ap_facts: the pins of the working specification, read once into globals.
ap_facts() {
  if ! [[ "$A_BLOB" =~ ^[0-9a-f]{40}$ ]]; then echo "the result blob of the approval record is not 40 lowercase hexadecimal digits" >&2; exit 2; fi
  AP_BASEBLOB=$(git rev-parse --verify --quiet "$BASE:$SPEC") || { echo "the specification is not on $BASE" >&2; exit 2; }
  git cat-file blob "$AP_BASEBLOB" > "$TMP/base.txt" 2> /dev/null || { echo "the base text cannot be read" >&2; exit 2; }
  AP_BLOB=$(git hash-object --no-filters "$SP")
  AP_SHA=$(sha256sum < "$SP" | cut -d ' ' -f1)
  AP_LINES=$(wc -l < "$SP" | tr -d ' ')
  AP_DIFF=$(git diff --no-index --shortstat -- "$TMP/base.txt" "$SP" | sed 's/^ *//')
  AP_COMM=$(git rev-list --count "$BASE..HEAD" -- "$SPEC" 2> /dev/null) || AP_COMM=""
  AP_REGBLOB=$(git hash-object --no-filters "$RG")
  AP_FPR=${AP_BLOB:0:12}
  AP_ADATE=$(line_val "- Owner reply date:" "$AR")
  if [ "$ROUND" -ge 5 ]; then
    if [ "$AD_OK" -ne 1 ]; then echo "cannot read $ADDENDUM" >&2; exit 2; fi
    AP_ADBLOB=$(git hash-object --no-filters "$AD")
  fi
}

# ap_pin_rows: the pin rows of the packet and of the record, in order.
ap_pin_rows() {
  printf '| Reviewed file | `%s` |\n' "$SPEC"
  printf '| Base blob | `%s` |\n' "$AP_BASEBLOB"
  printf '| Result blob | `%s` |\n' "$AP_BLOB"
  printf '| Reviewed SHA-256 | `%s` |\n' "$AP_SHA"
  printf '| Line count | `%s` |\n' "$AP_LINES"
  printf '| Diffstat | `%s` |\n' "$AP_DIFF"
  printf '| Commits touching the file | `%s` |\n' "$AP_COMM"
  printf '| Previously approved blob and SHA-256 | `%s` and `%s` |\n' "$A_BLOB" "$A_SHA"
  printf '| Register file | `%s` |\n' "$FREG_DEFAULT"
  printf '| Register blob | `%s` |\n' "$AP_REGBLOB"
  if [ "$ROUND" -ge 5 ]; then
    printf '| Disposition addendum file | `%s` |\n' "$DADD_PATH"
    printf '| Disposition addendum blob | `%s` |\n' "$AP_ADBLOB"
  fi
}

# aq_q N: the question N (1 to 4) as the owner is asked it.
aq_q() {
  case "$1" in
    1) printf 'Do you approve the new text exactly as it now stands (fingerprint %s, %s lines), or do you want changes?' "$AP_FPR" "$AP_LINES" ;;
    2) printf 'What would you like changed? Say it in your own words.' ;;
    3) printf 'Under which name should this approval be recorded?' ;;
    4) printf 'Which date should be recorded? Use the form YYYY-MM-DD.' ;;
  esac
}

print_aq() {
  local i
  for i in 1 2 3 4; do
    if [ "$i" -gt 1 ]; then printf '\n'; fi
    printf 'Q0%s %s\n%s\n' "$i" "${AQ_HEADS[$((i - 1))]}" "$(aq_q "$i")"
    if [ "$i" -eq 1 ]; then
      printf '%s: %s\n%s: %s\n' "$OPT_APPROVE" "$OPT_APPROVE_DESC" "$OPT_CHANGES" "$OPT_CHANGES_DESC"
    fi
  done
}

# make_delta: the hunks of the change from the round-1 text to the working specification in $TMP/delta.txt.
# Return 0, 2 when the two texts are equal, 3 when the previously approved text cannot be read.
make_delta() {
  git cat-file blob "$A_BLOB" > "$T1" 2> /dev/null || return 3
  if cmp -s "$T1" "$SP"; then return 2; fi
  git diff --no-index --no-color --no-ext-diff --no-textconv --unified=3 --diff-algorithm=myers --indent-heuristic -- "$T1" "$SP" \
    | awk '/^@@/ { on = 1 } on' > "$TMP/delta.txt"
  [ -s "$TMP/delta.txt" ] || return 2
  return 0
}

# ap_ready: succeed when the packet can be printed; print the reason to stderr otherwise.
ap_ready() {
  local n st
  n=$(wc -l < "$TMP/reg.rows" | tr -d ' ')
  if [ "$n" -ne "$NCHG" ]; then echo "the register does not hold $NCHG_W changes" >&2; return 1; fi
  st=$(cut -f5 "$TMP/reg.rows" | sort -u | tr '\n' ' ')
  if [ "$st" != "drafted " ]; then echo "not all $NCHG_W changes of the register are drafted" >&2; return 1; fi
  make_delta
  case $? in
    0) ;;
    2) echo "the working specification equals the text approved in round $((ROUND - 1)): there is no change to show" >&2; return 1 ;;
    *) echo "the round-$((ROUND - 1)) text cannot be read from the repository" >&2; return 1 ;;
  esac
  return 0
}

ap_reading() {
  if [ "$1" = repair ]; then printf 'repair: the text had one consistent reading'; else printf 'my choice: you can change it'; fi
}

# print_ask5: the paragraph "What you are asked" of profile 5. Every number and list is derived from the register
# (the number and the kinds of the changes) and from the disposition addendum (the answers on the related findings,
# one "id: word" pair for each block, in the order of the addendum).
print_ask5() {
  local lst k_od k_rep
  lst=$(awk '$0 ~ ("^### " pfx "-") { id = $2 } /^- Disposition: / && id != "" { w = $0; sub(/^- Disposition: /, "", w); printf "%s%s: %s", (n++ ? ", " : ""), id, w; id = "" }' pfx="$FPFX" "$AD")
  k_od=$(cut -f4 "$TMP/reg.rows" | grep -c -x -F 'owner decision')
  k_rep=$(cut -f4 "$TMP/reg.rows" | grep -c -x -F 'repair')
  printf 'On %s the owner approved the text of the specification. The independent reviewer then looked at it %s; the owner asked for the finding that the reviewer rated BLOCKING, its strongest rating, to be fixed, and answered the related findings that the disposition addendum records, each with the word the owner gave (%s).' "$AP_ADATE" "$AP_ORD" "$lst"
  if [ "$k_od" -gt 0 ]; then printf ' Where a change is of the kind owner decision the owner chose how.'; fi
  if [ "$k_rep" -gt 0 ]; then printf ' Where a change is of the kind repair the finding itself names the fix.'; fi
  printf ' The text has been changed in %s places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.\n\n' "$NCHG_W"
}

print_ap() {
  local n=0 g t f k total maxrun fl fence hunks added removed i
  total=$(wc -l < "$TMP/reg.rows" | tr -d ' ')
  printf '%s\n\n%s\n\n' "$AP_H1" "$AP_PENDING"
  printf '## What you are asked\n\n'
  if [ "$ROUND" -ge 5 ]; then
    print_ask5
  elif [ "$ROUND" -eq 4 ]; then
    printf 'On %s the owner approved the text of the specification. The independent reviewer then looked at it a third time; the owner asked for the three findings that the reviewer rated BLOCKING, its strongest rating, to be fixed. For two of them the owner chose how; for the third the finding itself names the fix. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.\n\n' "$AP_ADATE"
  elif [ "$ROUND" -eq 3 ]; then
    printf 'On %s the owner approved the text of the specification. The independent reviewer then looked at it a second time; the owner asked for the three findings that the reviewer rated BLOCKING, its strongest rating, to be fixed, and chose how. The text has been changed in three places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.\n\n' "$AP_ADATE"
  else
    printf 'On %s the owner approved the text of the specification. The independent reviewer then reported its findings, and the owner asked for eleven of them to be fixed. The text has been changed in nine places. This packet shows each change in plain words with the text before and after, then identifies the exact text, then shows the exact change line by line. You approve the text exactly as it now stands, or you ask for changes. Nothing is approved until you answer. An answer that differs from the text as shown is a request for changes.\n\n' "$AP_ADATE"
  fi
  printf '%s\n\n| # | What changed | Why | Whose reading |\n|---|---|---|---|\n' "$REG_TBL_H"
  while IFS=$'\t' read -r g _ _ k _ _ _; do
    n=$((n + 1))
    if [ "$ROUND" -ge 4 ] && [ "$k" = repair ]; then
      printf '| %s | %s | %s | %s |\n' "$n" "$(ev "$g" "What changed")" "$(ev "$g" "Why")" "$AP_NOASK_CELL"
    elif [ "$ROUND" -ge 3 ]; then
      printf '| %s | %s | %s | your decision: %s |\n' "$n" "$(ev "$g" "What changed")" "$(ev "$g" "Why")" "$(ev "$g" "Owner decision")"
    else
      printf '| %s | %s | %s | %s |\n' "$n" "$(ev "$g" "What changed")" "$(ev "$g" "Why")" "$(ap_reading "$k")"
    fi
  done < "$TMP/reg.rows"
  printf '\n## Before and after\n\n'
  n=0
  while IFS=$'\t' read -r g t f k _ _ _; do
    n=$((n + 1))
    printf '### Change %s of %s: %s\n\n' "$n" "$total" "$t"
    if [ "$ROUND" -ge 4 ] && [ "$k" = repair ]; then
      printf -- '- Findings: %s\n- Your decision: %s\n- Before: %s\n- After: %s\n\n' "$f" "$AP_NOASK_BULLET" "$(ev "$g" "Before")" "$(ev "$g" "After")"
    elif [ "$ROUND" -ge 3 ]; then
      printf -- '- Findings: %s\n- Options offered: %s\n- Your decision: %s; reason: %s\n- Before: %s\n- After: %s\n\n' "$f" "$(ev "$g" "Options")" "$(ev "$g" "Owner decision")" "$(ev "$g" "Owner reason")" "$(ev "$g" "Before")" "$(ev "$g" "After")"
    else
      printf -- '- Findings: %s\n- My choice: %s\n- Before: %s\n- After: %s\n\n' "$f" "$(ev "$g" "My choice")" "$(ev "$g" "Before")" "$(ev "$g" "After")"
    fi
  done < "$TMP/reg.rows"
  printf '## The text under approval\n\n| Field | Value |\n|---|---|\n'
  ap_pin_rows
  printf '\n## The exact change\n\n'
  hunks=$(grep -c '^@@' "$TMP/delta.txt")
  added=$(grep -c '^+' "$TMP/delta.txt")
  removed=$(grep -c '^-' "$TMP/delta.txt")
  printf 'The change from the text approved in round %s has %s hunks, adds %s lines and removes %s lines.\n\n' "$((ROUND - 1))" "$hunks" "$added" "$removed"
  maxrun=$(grep -o '`*' "$TMP/delta.txt" | awk '{ if (length($0) > m) m = length($0) } END { print m + 0 }')
  fl=3
  if [ "$maxrun" -ge 3 ]; then fl=$((maxrun + 1)); fi
  fence=""
  for ((i = 0; i < fl; i++)); do fence="$fence\`"; done
  printf '%s\n' "$fence"
  cat "$TMP/delta.txt"
  printf '%s\n\n' "$fence"
  printf '## Questions\n\n'
  for i in 1 2 3 4; do
    printf '### Q0%s — %s\n\n- Question: %s\n' "$i" "${AQ_HEADS[$((i - 1))]}" "$(aq_q "$i")"
    if [ "$i" -eq 1 ]; then
      printf -- '- Options:\n  - %s: %s\n  - %s: %s\n' "$OPT_APPROVE" "$OPT_APPROVE_DESC" "$OPT_CHANGES" "$OPT_CHANGES_DESC"
    fi
    printf -- '- Answer: (unanswered)\n\n'
  done
  printf '## What follows\n\n%s\n\n%s\n\n%s\n\n%s\n' "$AP_FOLLOWS_1" "$AP_FOLLOWS_2" "$AP_FOLLOWS_3" "$AP_CLOSING"
}

# pk_pending FILE OUT: the packet read as its pending form.
pk_pending() {
  sed "s/^$AP_RECORDED\$/$AP_PENDING/" "$1" > "$2"
}

print_ars() {
  local i
  if [ "$(grep -c '^- Owner approval:' "$PK")" -ne 1 ] || ! grep -q -x -F -e "$AP_PENDING" "$PK"; then
    echo "cannot print the record skeleton: the packet status line is not exactly [$AP_PENDING]" >&2
    exit 2
  fi
  printf '%s\n\n' "$AR_H1"
  printf -- '- Owner approval: %s\n- Owner reply date: %s\n\n' "$FILL" "$FILL"
  printf '| Field | Value |\n|---|---|\n'
  ap_pin_rows
  printf '| Packet file | `%s` |\n' "$PACKET_DEFAULT"
  printf '| Packet blob | `%s` |\n' "$(git hash-object --no-filters "$PK")"
  printf '| Packet SHA-256 | `%s` |\n' "$(sha256sum < "$PK" | cut -d ' ' -f1)"
  printf '| Reply given by | %s |\n| Owner reply | %s |\n| Check results | %s |\n\n' "$FILL" "$FILL" "$FILL"
  printf '## Questions and answers\n\n'
  for i in 1 2 3 4; do
    printf '### Q0%s — %s\n\n- Question: %s\n- Answer: %s\n\n' "$i" "${AQ_HEADS[$((i - 1))]}" "$(aq_q "$i")" "$FILL"
  done
  printf '## What follows\n\n%s\n\n%s\n' "$FILL" "$AR_CLOSING"
}

# tbl_tokens: the hash-like backticked tokens of the table rows on stdin, separated by spaces.
tbl_tokens() {
  { grep '^| ' | grep -o '`[0-9A-Fa-f]\{7,\}`' | tr -d '`' | sort -u | tr '\n' ' '; } || true
}

# ---- stage approval-pending ----

approval_pending_stage() {
  local m t w i h out rc last n st
  ap_facts
  reg_load

  # AP1
  m=$(enc1 "$ID")
  if [ -z "$m" ]; then m=$(enc2 "$ID"); fi
  parse_pins "$ID" "$TMP/id.pins"
  for t in "Result blob" "Reviewed SHA-256" "Line count" "Diffstat" "Base blob" "Check results"; do
    if [ -z "$m" ] && [ "$(pin_count "$TMP/id.pins" "$t")" -ne 1 ]; then m="the identity note does not hold the row [$t] exactly once"; fi
  done
  if [ -z "$m" ]; then
    if [ "$(pin_tok "$TMP/id.pins" "Result blob")" != "$AP_BLOB" ]; then m="the Result blob row of the identity note differs from the working specification ($AP_BLOB)"
    elif [ "$(pin_tok "$TMP/id.pins" "Reviewed SHA-256")" != "$AP_SHA" ]; then m="the Reviewed SHA-256 row of the identity note differs from the working specification"
    elif [ "$(pin_raw "$TMP/id.pins" "Line count")" != "$AP_LINES" ]; then m="the Line count row of the identity note differs from the working specification ($AP_LINES)"
    elif [ "$(pin_raw "$TMP/id.pins" "Diffstat")" != "$AP_DIFF" ]; then m="the Diffstat row of the identity note differs from the working specification ($AP_DIFF)"
    elif [ "$(pin_tok "$TMP/id.pins" "Base blob")" != "$AP_BASEBLOB" ]; then m="the Base blob row of the identity note differs from the specification on $BASE ($AP_BASEBLOB)"
    elif ! has "$(pin_raw "$TMP/id.pins" "Check results")" 'RESULT: PASS'; then m="the Check results row of the identity note does not quote RESULT: PASS"
    fi
  fi
  if [ -z "$m" ]; then
    i=$(git rev-parse --verify --quiet ":$SPEC" 2> /dev/null) || i=""
    h=$(git rev-parse --verify --quiet "HEAD:$SPEC" 2> /dev/null) || h=""
    w=$(git hash-object --no-filters -- "$SPECFILE" 2> /dev/null) || w=""
    if [ "$w" != "$AP_BLOB" ] || [ "$i" != "$AP_BLOB" ] || [ "$h" != "$AP_BLOB" ]; then
      m="the working file, the index and HEAD do not hold one blob for the specification ([$w] [$i] [$h])"
    fi
  fi
  if [ -n "$m" ]; then fail AP1 "$m"; else pass AP1 "the identity note equals the working specification ($AP_BLOB, $AP_LINES lines) and the file, the index and HEAD agree"; fi

  # AP2
  m=""
  pk_pending "$PK" "$TMP/packet.pend"
  if ! ap_ready 2> "$TMP/ap.err"; then
    m="the packet cannot be printed: $(head -n1 "$TMP/ap.err")"
  else
    print_ap > "$TMP/packet.exp"
    if ! cmp -s "$TMP/packet.exp" "$TMP/packet.pend"; then
      m="the packet differs from the printed one (first difference: $(diff "$TMP/packet.exp" "$TMP/packet.pend" | grep '^[<>]' | head -n1 | cut -c1-80))"
    fi
  fi
  if [ -n "$m" ]; then fail AP2 "$m"; else pass AP2 "the packet equals the output of --print-approval-packet byte for byte"; fi

  # AP3
  m=$(enc1 "$PK")
  if [ -z "$m" ]; then m=$(enc2 "$PK"); fi
  if [ -z "$m" ]; then m=$(fd1_scan "$PK" "$(h2sec "$PK" "The text under approval" | tbl_tokens) $AP_FPR"); fi
  if [ -n "$m" ]; then fail AP3 "$m"; else pass AP3 "the packet is valid UTF-8 without byte order mark, LF only, and passes the self-containment scan"; fi

  # AP4
  m=""
  local eargs=()
  if [ "$ROUND" -ge 5 ]; then eargs=(--addendum "$ADDENDUM"); fi
  out=$(bash "$SELF" --round "$ROUND" --stage edits --complete --register "$REGISTER" --spec "$SPECFILE" --base "$BASE" ${eargs[@]+"${eargs[@]}"} 2>&1)
  rc=$?
  last=$(printf '%s\n' "$out" | tail -n1)
  if [ "$rc" -ne 0 ] || [ "$last" != "RESULT: PASS" ]; then m="the stage edits with --complete does not pass ($last)"; fi
  if [ "$SPECFILE" != "$SPEC" ]; then
    out=$(bash "$CHK2" --final --file "$SPECFILE" 2>&1)
  else
    out=$(bash "$CHK2" --final 2>&1)
  fi
  rc=$?
  last=$(printf '%s\n' "$out" | tail -n1)
  if [ "$rc" -ne 0 ] || [ "$last" != "RESULT: PASS" ]; then m="${m:+$m; }the Phase 2 check with --final does not pass ($last)"; fi
  if [ -n "$m" ]; then fail AP4 "$m"; else pass AP4 "the stage edits with --complete and the Phase 2 check with --final end RESULT: PASS"; fi

  # AP5
  m=""
  n=$(grep -c '^- Owner approval:' "$PK")
  st=$(grep '^- Owner approval:' "$PK" | head -n1)
  if [ "$n" -ne 1 ]; then
    m="the packet holds $n status lines, expected one"
  elif [ "$st" = "$AP_PENDING" ]; then
    :
  elif [ "$st" = "$AP_RECORDED" ] && [ -f "$RECORD" ]; then
    :
  else
    m="the packet status line is [$st], expected the pending form (the recorded form only when the record exists)"
  fi
  if [ -n "$m" ]; then fail AP5 "$m"; else pass AP5 "the packet status line is consistent with the existence of the record"; fi
}

# ---- stage approval-recorded ----

approval_recorded_stage() {
  local m i expq blk out dt drdate nm pk_blob pk_sha exp_h3 rec_h3 q1 q2 q3 q4 allowed
  ap_facts
  reg_load
  pk_pending "$PK" "$TMP/packet.pend"
  pk_blob=$(git hash-object --no-filters "$TMP/packet.pend")
  pk_sha=$(sha256sum < "$TMP/packet.pend" | cut -d ' ' -f1)
  parse_pins "$RC" "$TMP/rc.pins"
  exp_h3=$(for i in 1 2 3 4; do printf '### Q0%s — %s\n' "$i" "${AQ_HEADS[$((i - 1))]}"; done)
  rec_h3=$(grep '^### ' "$RC")
  out=$(line_val "- Owner approval:" "$RC")
  dt=$(line_val "- Owner reply date:" "$RC")

  # AR1
  m=$(enc1 "$RC")
  if [ -z "$m" ]; then m=$(enc2 "$RC"); fi
  if [ -z "$m" ] && grep -q -F "$FILL" "$RC"; then m="a fill marker is left (line $(grep -n -F "$FILL" "$RC" | head -n1 | cut -d: -f1))"; fi
  if [ -z "$m" ]; then
    allowed="$(tbl_tokens < "$RC") $AP_FPR $pk_blob $pk_sha"
    m=$(fd1_scan "$RC" "$allowed")
  fi
  if [ -z "$m" ]; then
    if [ "$(head -n1 "$RC")" != "$AR_H1" ]; then m="the first line is not the H1 [$AR_H1]"
    elif [ "$(grep -c '^- Owner approval:' "$RC")" -ne 1 ]; then m="the record does not hold exactly one line [- Owner approval:]"
    elif [ "$out" != approved ] && [ "$out" != "changes requested" ]; then m="the outcome [$out] is neither approved nor changes requested"
    elif [ "$(grep -c '^- Owner reply date:' "$RC")" -ne 1 ]; then m="the record does not hold exactly one line [- Owner reply date:]"
    elif [ "$rec_h3" != "$exp_h3" ]; then m="the question blocks are not Q01 to Q04 once each in order"
    elif [ "$(grep '^## ' "$RC" | tr '\n' '|')" != "## Questions and answers|## What follows|" ]; then m="the H2 headings are not Questions and answers and What follows"
    elif [ "$(tail -n1 "$RC")" != "$AR_CLOSING" ] || [ "$(grep -c -x -F "$AR_CLOSING" "$RC")" -ne 1 ]; then m="the closing line is not the last line, once"
    fi
  fi
  if [ -n "$m" ]; then fail AR1 "$m"; else pass AR1 "the record is clean text without fill markers, passes the scan and has the expected structure"; fi

  # AR2
  m=""
  if ! ap_ready 2> /dev/null; then
    m="the packet cannot be printed"
  else
    print_ap > "$TMP/packet.exp"
    { ap_pin_rows
      printf '| Packet file | `%s` |\n| Packet blob | `%s` |\n| Packet SHA-256 | `%s` |\n' "$PACKET_DEFAULT" "$pk_blob" "$pk_sha"
    } > "$TMP/rows.exp"
    grep '^| ' "$RC" | grep -v -e '^| Field ' -e '^|[-| ]*$' | head -n "$(wc -l < "$TMP/rows.exp" | tr -d ' ')" > "$TMP/rows.rec"
    if ! cmp -s "$TMP/rows.exp" "$TMP/rows.rec"; then
      m="the pin rows differ from those computed from the live text and the packet (first difference: $(diff "$TMP/rows.exp" "$TMP/rows.rec" | grep '^[<>]' | head -n1 | cut -c1-80))"
    elif ! cmp -s "$TMP/packet.exp" "$TMP/packet.pend"; then
      m="the packet differs from the printed one (first difference: $(diff "$TMP/packet.exp" "$TMP/packet.pend" | grep '^[<>]' | head -n1 | cut -c1-80))"
    fi
  fi
  if [ -n "$m" ]; then fail AR2 "$m"; else pass AR2 "the pin rows equal those computed from the live text, the previously approved pins and the packet, and the packet is the printed one"; fi

  # AR3
  m=""
  for i in 1 2 3 4; do
    blk="$TMP/q$i.blk"
    h3blk "$RC" "### Q0$i — ${AQ_HEADS[$((i - 1))]}" > "$blk"
    expq="- Question: $(aq_q "$i")"
    if [ "$(grep -c '^- Question: ' "$blk")" -ne 1 ] || [ "$(grep '^- Question: ' "$blk")" != "$expq" ]; then
      m="${m:+$m; }the Question bullet of Q0$i differs from the printed one"
    fi
  done
  if [ -n "$m" ]; then fail AR3 "$m"; else pass AR3 "the four Question bullets equal the printed questions"; fi

  # AR4
  m=""
  for i in 1 2 3 4; do
    if [ "$(grep -c '^- Answer: ' "$TMP/q$i.blk")" -ne 1 ]; then m="${m:+$m; }Q0$i does not hold exactly one Answer line"; fi
  done
  q1=$(line_val "- Answer:" "$TMP/q1.blk")
  q2=$(line_val "- Answer:" "$TMP/q2.blk")
  q3=$(line_val "- Answer:" "$TMP/q3.blk")
  q4=$(line_val "- Answer:" "$TMP/q4.blk")
  if [ -z "$m" ]; then
    if [ "$q1" != "$OPT_APPROVE" ] && [ "$q1" != "$OPT_CHANGES" ]; then
      m="the answer of Q01 [$q1] is neither [$OPT_APPROVE] nor [$OPT_CHANGES]"
    elif [ "$q1" = "$OPT_APPROVE" ] && [ "$q2" != "$NOT_ASKED" ]; then
      m="Q01 is [$OPT_APPROVE] but the answer of Q02 is not the sentence [$NOT_ASKED]"
    elif [ "$q1" = "$OPT_CHANGES" ] && { [ -z "$(trim_ws "$q2")" ] || [ "$q2" = "$NOT_ASKED" ]; }; then
      m="Q01 is [$OPT_CHANGES] but the answer of Q02 is empty or the not-asked sentence"
    elif [ "$q1" = "$OPT_APPROVE" ] && [ "$out" != approved ]; then
      m="Q01 is [$OPT_APPROVE] but the outcome is [$out], expected approved"
    elif [ "$q1" = "$OPT_CHANGES" ] && [ "$out" != "changes requested" ]; then
      m="Q01 is [$OPT_CHANGES] but the outcome is [$out], expected changes requested"
    fi
  fi
  if [ -n "$m" ]; then fail AR4 "$m"; else pass AR4 "the answers of Q01 and Q02 and the outcome [$out] follow the rule"; fi

  # AR5
  m=""
  nm=$(pin_raw "$TMP/rc.pins" "Reply given by")
  drdate=$(line_val "- Owner disposition date:" "$DR")
  if [ "$ROUND" -ge 5 ]; then drdate=$(line_val "- Owner disposition date:" "$AD"); fi
  if [ -z "$(trim_ws "$q3")" ] || [ "$q3" != "$(trim_ws "$q3")" ]; then
    m="the name (the answer of Q03) is empty or padded"
  elif [ "$(pin_count "$TMP/rc.pins" "Reply given by")" -ne 1 ] || [ "$nm" != "$q3" ]; then
    m="the Reply given by row is missing or differs from the answer of Q03"
  elif ! [[ "$q4" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]] || [ "$(date -u -d "$q4" +%F 2> /dev/null)" != "$q4" ]; then
    m="the date [$q4] is not a valid calendar date in the form YYYY-MM-DD"
  elif [ "$dt" != "$q4" ]; then
    m="the Owner reply date line [$dt] differs from the answer of Q04 [$q4]"
  elif ! [[ "$drdate" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
    m="the owner disposition date of the disposition record is not a date"
  elif [[ "$q4" < "$drdate" ]] && [ "$ROUND" -ge 5 ]; then
    m="the date [$q4] is earlier than the owner disposition date of the addendum of round $ADD_RND [$drdate]"
  elif [[ "$q4" < "$drdate" ]]; then
    m="the date [$q4] is earlier than the owner disposition date of round $((ROUND - 1)) [$drdate]"
  elif [ "$(pin_count "$TMP/rc.pins" "Owner reply")" -ne 1 ] || [ -z "$(trim_ws "$(pin_raw "$TMP/rc.pins" "Owner reply")")" ]; then
    m="the Owner reply row is missing or empty"
  fi
  if [ -n "$m" ]; then fail AR5 "$m"; else pass AR5 "the name and the date are complete and consistent, and the date is not earlier than $drdate"; fi
}

if [ "$PRINT_DELTA" -eq 1 ] && [ "$AP_ON" -eq 1 ]; then
  make_delta
  case $? in
    0) cat "$TMP/delta.txt"; exit 0 ;;
    2) echo "the working specification equals the text approved in round $((ROUND - 1))" >&2; exit 2 ;;
    *) echo "the round-$((ROUND - 1)) text cannot be read from the repository" >&2; exit 2 ;;
  esac
fi
if [ "$PRINT_AQ" -eq 1 ] && [ "$AP_ON" -eq 1 ]; then
  ap_facts
  print_aq
  exit 0
fi
if [ "$PRINT_APK" -eq 1 ] && [ "$AP_ON" -eq 1 ]; then
  ap_facts
  reg_load
  ap_ready || exit 2
  print_ap
  exit 0
fi
if [ "$PRINT_ARS" -eq 1 ] && [ "$AP_ON" -eq 1 ]; then
  ap_facts
  print_ars
  exit 0
fi

if [ "$REPLAY" -eq 1 ]; then
  if [ "$RP5" -eq 1 ]; then replay5; elif [ "$RP4" -eq 1 ]; then replay4; elif [ "$RP3" -eq 1 ]; then replay3; elif [ "$RP2" -eq 1 ]; then replay2; else replay; fi
  finish
fi

if [ "$AP_ON" -eq 1 ] && [ "$STAGE" = approval-pending ]; then
  approval_pending_stage
  finish
fi

if [ "$AP_ON" -eq 1 ] && [ "$STAGE" = approval-recorded ]; then
  approval_recorded_stage
  finish
fi

if [ "$STAGE" = state ]; then
  state_stage
  finish
fi

if [ "$STAGE" = edits ]; then
  edits_stage
  finish
fi

if [ "$STAGE" = dispositions ]; then
  da_checks
  finish
fi

decisions_stage
finish
