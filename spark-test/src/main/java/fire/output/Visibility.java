package fire.output;

public enum Visibility {
    EXPANDED,
    COLLAPSED;

    private String name = this.name().toLowerCase();

    private Visibility() {
    }

    public String getName() {
        return this.name;
    }
}
