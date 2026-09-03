# Content classes

Every durable entry has one authority class.

| Class | Meaning | May change baseline? |
|---|---|---|
| `reference` | Externally published source or method orientation | No |
| `baseline` | DigitalIE clean-room guidance accepted for general use | Yes, through reviewed revision |
| `observation` | Sanitized statement about a practice or outcome | No |
| `candidate` | Proposed learning with rationale and evidence class | No |
| `adopted-practice` | Deliberately promoted guidance for a declared scope | Only within that scope |
| `superseded` | Retained historical entry replaced by another | No |
| `rejected` | Considered proposal that did not pass review | No |

AI-generated text is a draft, not a content class. Its claims must resolve to one of the classes above.

## Target metadata contract

Once metadata enforcement is enabled for a content class, each governed entry identifies `id`, `type`, `status`, `scope`, `source_class`, `owner`, `review_by`, `supersedes`, and related entries. Until the staged rollout is complete, directory placement and the content-class rules remain authoritative; missing metadata must be reported rather than inferred.
