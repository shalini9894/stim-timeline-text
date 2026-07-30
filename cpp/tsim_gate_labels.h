#ifndef _STIM_DIAGRAM_TSIM_GATE_LABELS_H
#define _STIM_DIAGRAM_TSIM_GATE_LABELS_H

#include <optional>
#include <string>
#include <string_view>

namespace tsim_labels {

/// Decodes a tsim metadata tag into the logical gate label it represents.
/// Returns nullopt when the tag is not tsim's, so the caller keeps Stim's
/// own gate name untouched.
std::optional<std::string> logical_label(std::string_view tag, std::string_view stim_gate_name);

}  // namespace tsim_labels

#endif
