#include "tsim_gate_labels.h"

#include <vector>

namespace tsim_labels {

static std::string_view trim(std::string_view s) {
    size_t b = 0, e = s.size();
    while (b < e && (s[b] == ' ' || s[b] == '\t')) b++;
    while (e > b && (s[e - 1] == ' ' || s[e - 1] == '\t')) e--;
    return s.substr(b, e - b);
}

static bool is_t_tag(std::string_view tag) {
    return tag == "T" || (tag.size() > 2 && tag.substr(0, 2) == "T:");
}

static std::optional<std::string> t_family_label(std::string_view gate) {
    if (gate == "S") return std::string("T");
    if (gate == "S_DAG") return std::string("T_DAG");
    if (gate == "SPP") return std::string("TPP");
    if (gate == "SPP_DAG") return std::string("TPP_DAG");
    return std::nullopt;
}

static bool is_known_parametric(std::string_view name) {
    return name == "R_X" || name == "R_Y" || name == "R_Z" ||
           name == "U3" || name == "R_PAULI";
}

std::optional<std::string> logical_label(std::string_view tag, std::string_view stim_gate_name) {
    if (tag.empty()) {
        return std::nullopt;
    }
    if (is_t_tag(tag)) {
        return t_family_label(stim_gate_name);
    }

    size_t open = tag.find('(');
    if (open == std::string_view::npos || tag.back() != ')') {
        return std::nullopt;
    }
    std::string_view name = tag.substr(0, open);
    if (!is_known_parametric(name)) {
        return std::nullopt;
    }
    std::string_view body = tag.substr(open + 1, tag.size() - open - 2);

    std::vector<std::string_view> values;
    size_t start = 0;
    while (start <= body.size()) {
        size_t comma = body.find(',', start);
        size_t count = (comma == std::string_view::npos) ? std::string_view::npos : comma - start;
        std::string_view part = trim(body.substr(start, count));
        if (!part.empty()) {
            size_t eq = part.find('=');
            if (eq == std::string_view::npos) {
                return std::nullopt;
            }
            std::string_view value = part.substr(eq + 1);
            if (value.size() < 3 || value.substr(value.size() - 3) != "*pi") {
                return std::nullopt;
            }
            values.push_back(value.substr(0, value.size() - 3));
        }
        if (comma == std::string_view::npos) {
            break;
        }
        start = comma + 1;
    }

    if (values.empty()) {
        return std::nullopt;
    }

    std::string out(name);
    out += "(";
    for (size_t k = 0; k < values.size(); k++) {
        if (k > 0) out += ",";
        out.append(values[k]);
    }
    out += ")";
    return out;
}

}  // namespace tsim_labels
